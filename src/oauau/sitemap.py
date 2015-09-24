from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse


class OauauSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return ['landing_page']

    def location(self, item):
        return reverse(item)
