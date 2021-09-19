# Some Misc code that you may find useful for certain use cases in your website.

#-------------------------------------------------------------------------------
#   formatChecker.py - Checks file format and size of user uploaded files.
from django.db.models import FileField
from django.forms import forms
from django.template.defaultfilters import filesizeformat
import ast
import mimetypes

#Only file types shown here will be allowed to be uploaded to the website
content_types = ['application/zip', 'application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'application/vnd.ms-excel','application/vnd.openxmlformats-officedocument.spreadsheetml.sheet','application/vnd.ms-excel.sheet.macroEnabled.12',
                'application/vnd.ms-powerpoint','application/vnd.openxmlformats-officedocument.presentationml.presentation','application/x-zip-compressed']

#Currently max size set to 50MB
max_upload_size = 52428800

class ContentTypeRestrictedFileField(FileField):
    """
    Same as FileField, but you can specify:
        * content_types - list containing allowed content_types. Example: ['application/pdf', 'image/jpeg']
        * max_upload_size - a number indicating the maximum file size allowed for upload.
            2.5MB - 2621440
            5MB - 5242880
            10MB - 10485760
            20MB - 20971520
            50MB - 52428800
            100MB 104857600
            250MB - 214958080
            500MB - 429916160
    """

    def clean(self, *args, **kwargs):
        data = super(ContentTypeRestrictedFileField, self).clean(*args, **kwargs)

        file = data.file
        try:
            content_type = file.content_type
            if content_type in content_types:
                if file.size > max_upload_size:
                    raise forms.ValidationError(('Please keep filesize under %s. Current filesize %s') % (filesizeformat(max_upload_size), filesizeformat(file.size)))
            else:
                raise forms.ValidationError(('Filetype not supported.'))
        except AttributeError:
            pass

        return data
      

      

#-------------------------------------------------------------------------------
#   downloadZIP view - ZIP all of a users files into one for convenient download
#   To implement, you will need to add this to the view of the relevant web app
#   and edit to fit your file naming conventions
def downloadZIP(request, username):
    file_path = os.path.join(settings.MEDIA_ROOT, formName)
    # Checks that the user, whose files are being requested, actually exists
    user = get_object_or_404(UserInfo, username=username)

    # Retrieve all files belonging to the user
    uFile = userFiles.objects.filter(name__icontains=username)
    if not uFile:
        return HttpResponse('User has not uploaded any files')
    else:

        # Open BytesIO to grab in-memory ZIP contents
        s = BytesIO()

        # The zip compressor
        zf = zipfile.ZipFile(s, "w")

        for file in uFile:

            # Add file, at correct path
            name = file.newfile.path.split('/')[-1]
            zf.write(file.newfile.path, name)

        # Must close zip for all contents to be written
        zf.close()

        # Grab ZIP file from in-memory, make response with correct MIME-type
        resp = HttpResponse(s.getvalue(), content_type = 'application/x-zip-compressed')
        # ..and correct content-disposition
        resp['Content-Disposition'] = 'attachment; filename=%s' % username+'_'+formName+'.zip'

        return resp
