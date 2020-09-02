from boxsdk import JWTAuth

# JWT access appears to come from the Service Account for the application.
# Any API calls made with this token will seem to come from this application
# and will not have access to files and folders without getting access
# from them.

# A key aspect of JWT auth is signing requests using an rsa keypair.
# To generate an rsa keypair, go into the box console, select your application,
# click Configuration in the sidebar, and there is a Add and Manage Public
# Keys section.  Clicking this will trigger a download.  Save the .json file
# to disk and reference it below.

# Note: if JWTAuth appears to be None, YOU ARE MISSING the boxsdk[jwt] PIP PACKAGE.
# Note2: who the heck names a package like "boxsdk[jwt]"???

auth = JWTAuth.from_settings_file('615094728_5gxxpqrs_config.json')

access_token = auth.authenticate_instance()

from boxsdk import Client, BoxAPIException
from boxsdk.object.collaboration import CollaborationRole

client = Client(auth)
print(client)
user = client.user().get()
print(user)
print("The service account user's email is {}".format(user.login))

# Note3: If you get the message "This app is not authorized by the enterprise admin",
#  the application is not yet approved.  You have to get it approved before you can
#  do anything further.


# The root folder can be listed, and files stored here.  They will be invisible to
# anyone other than this service account.
root_folder = client.folder('0')
print(root_folder)
print([(i.type, i.id, i.name) for i in root_folder.get_items()])

def upload_file_to_external_folder():
    # I created a folder in my personal box account called "test" and shared it with the
    # service account by using the .login (email address) printed above.  It has the id
    # 122011345352
    test_folder = client.folder('122011345352')

    # Let's upload a file to that shared folder so we can see it in the Box webapp.
    from io import StringIO
    s = StringIO()
    s.write('hello world from the python box sdk api')
    s.seek(0)
    box_file = client.folder('122011345352').upload_stream(s, 'hello_world.txt')
    print('File {0} uploaded to box with file id {1}'.format(box_file.name, box_file.id))
    print(box_file.name)
    print(box_file.content())
    print(box_file.id)

    print([(i.type, i.id, i.name) for i in test_folder.get_items()])

def get_item_by_name(items, name):
    ''' Get the item with the desired name. '''
    for item in items:
        if item.name == name:
            return item
    return None

def add_collaborator():
    # Create a folder for sharing out with others
    try:
        root_folder.create_subfolder('service_account_share')
    except BoxAPIException as e:
        pass
    folder = get_item_by_name(root_folder.get_items(), 'service_account_share')

    # Collaborators can be specified by user, group, or email address
    role = CollaborationRole.EDITOR
    # collaborator = 'email_address_goes_here'
    folder.add_collaborator(collaborator, role)

    # At this point, the 'service_account_share' folder appears in the
    # users root folder.


#upload_file_to_external_folder()
#add_collaborator()

