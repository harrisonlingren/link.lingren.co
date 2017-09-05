# [START vendor]
from google.appengine.ext import vendor
print 'libraries added?'
# Add any libraries installed in the "lib" folder.
vendor.add('lib')
# [END vendor]
print 'libraries added!'
