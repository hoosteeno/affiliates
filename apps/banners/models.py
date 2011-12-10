from django.conf import settings
from django.db import models

import jingo
from caching.base import CachingManager, CachingMixin
from funfactory.manage import path
from funfactory.urlresolvers import reverse
from tower import ugettext_lazy as _lazy

from badges.models import Badge, BadgeInstance
from banners import COLOR_CHOICES
from shared.models import LocaleField, ModelBase
from shared.utils import absolutify


# L10n: Width and height are the width and height of an image.
SIZE = _lazy('%(width)sx%(height)s pixels')


BANNER_TEMPLATE_FILE = 'apps/banners/templates/banners/banner_template.html'
with open(path(BANNER_TEMPLATE_FILE)) as f:
    BANNER_TEMPLATE = f.read()


class Banner(Badge):
    """Badge consisting of an image link."""
    customize_view = 'banners.views.customize_banner'

    objects = CachingManager()

    def customize_url(self):
        return reverse('banners.customize', kwargs={'banner_pk': self.pk})


class BannerImage(CachingMixin, ModelBase):
    """Image that a user can choose for their specific banner."""
    banner = models.ForeignKey(Banner)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES,
                             verbose_name=u'image color')
    image = models.ImageField(upload_to=settings.BANNER_IMAGE_PATH,
                              verbose_name=u'image file',
                              max_length=settings.MAX_FILEPATH_LENGTH)
    locale = LocaleField()

    objects = CachingManager()

    @property
    def size(self):
        """Return a string representing the size of this image in pixels."""
        if self.image:
            return SIZE % {'width': self.image.width,
                           'height': self.image.height}
        else:
            return u''

    def __unicode__(self):
        return '%s: %s %s' % (self.banner.name, self.color, self.size)


class BannerInstance(BadgeInstance):
    image = models.ForeignKey(BannerImage)

    details_template = 'banners/details.html'

    def render(self):
        return jingo.env.from_string(BANNER_TEMPLATE).render({
            'url': self.affiliate_link(),
            'img': absolutify(self.image.image.url)
        })

    def affiliate_link(self):
        return reverse('banners.link', kwargs={'user_id': self.user.pk,
                                               'banner_id': self.badge.pk,
                                               'banner_img_id': self.image.pk})
