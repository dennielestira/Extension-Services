from cloudinary_storage.storage import RawMediaCloudinaryStorage

class PublicRawStorage(RawMediaCloudinaryStorage):
    def _get_cloudinary_options(self, options):
        opts = super()._get_cloudinary_options(options)
        opts['access_mode'] = 'public'
        return opts
