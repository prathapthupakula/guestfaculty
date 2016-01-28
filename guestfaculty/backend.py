from django.contrib.auth.backends import RemoteUserBackend
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.conf import settings
import ldap

class GFRemoteUserBackend (RemoteUserBackend):
    # Create a User object if not already in the database?
    create_unknown_user = True

    def configure_user(self,user):

        # Get User Settings from LDAP and setup Local Account
	
        lapp = ldap.initialize(settings.LDAP_SERVER)
        try:
            l_user = lapp.search_s(settings.LDAP_BASE_DN, ldap.SCOPE_SUBTREE, "uid=%s" % user)
            # Because LDAP returns results in the form:
            # [[dn, details], [dn, details], ...]
            dn = l_user[0][0]
            new_user_details = l_user[0][1]
        except:
            l_user = {} # empty
        finally:
            lapp.unbind_s()
		
        if new_user_details!={}:
            sso_uname = new_user_details["cn"]
            sso_role = new_user_details["employeeType"][0]
            role1 = ''.join(sso_role.split())
            role=(role1.lower())
            user.first_name = sso_uname[0].split()[0]
            user.last_name = sso_uname[0].split()[1]
            user.email = new_user_details["uid"][0]
            user.is_staff = True
            if Group.objects.filter(name=role):
                user.groups.add(Group.objects.get(name=role))
            user.set_unusable_password()
            user.save()
        return user
