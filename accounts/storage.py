from cloudinary_storage.storage import MediaCloudinaryStorage
import cloudinary.uploader

class RawMediaCloudinaryStorage(MediaCloudinaryStorage):
    """Custom storage that handles all file types including ZIP, PDF, DOCX, etc."""
    
    def _upload(self, name, content):
        """Upload files as 'raw' resource type to support all formats."""
        
        # Get folder from the upload path
        folder = '/'.join(name.split('/')[:-1]) if '/' in name else ''
        
        options = {
            'resource_type': 'raw',  # This is the key - allows ZIP and all file types
            'folder': folder,
            'use_filename': True,
            'unique_filename': True,
            'overwrite': False,
        }
        
        try:
            response = cloudinary.uploader.upload(content, **options)
            return response
        except Exception as e:
            print(f"Cloudinary upload error: {str(e)}")
            raise