import ldap3

# Define LDAP server connection details
ip_address = "10.1.2.14"
port = 636   # Or 636 for LDAPS (LDAP over SSL/TLS)
username = "LDAPUser"
password = "S@lus.11" 

# Define LDAP server URL
server_url = f"ldaps://{ip_address}:{port}"

# Create a connection to the LDAP server to query
ldap_conn = ldap3.Connection(
    ldap3.Server(server_url),
    user=username,
    password=password,
    auto_bind=True,
)

# Check if the connection is successful
if ldap_conn.bound:
    print("LDAP server connection successful.")
else:
    print("LDAP server connection failed.")

username = 'Drextest'
user_password = 'Salus2023!'

ldap_conn.search('OU=Salus USERS,DC=ad,DC=salus,DC=edu', '(sAMAccountName=' + username + ')')

#Format DN to attempt user bind credentials
string = str(ldap_conn.entries[0])
temp = string.split('-')[0].split(':')
test_dn = temp[1].strip()

#Attempt a bind to verify user credentials given
user_ldap_conn = ldap3.Connection(
    ldap3.Server(server_url),
    user=test_dn,
    password=user_password,
    authentication="SIMPLE",
)


if not user_ldap_conn.bind(): #If not authenticated
    print("Error in bind", user_ldap_conn.result)
else: #If authenticated, check for permissions
    print("Valid authentication, checking for group")
    ldap_conn.search('OU=Salus USERS,DC=ad,DC=salus,DC=edu', '(&(objectCategory=user)(memberOf=CN=EIAdmin,OU=Salus GROUPS,DC=ad,DC=salus,DC=edu)(sAMAccountName=' + username + '))')
    #isAdminUser
    if len(ldap_conn.entries) < 1:
        print('User is not an admin.')
    else:
        print('User is an admin')

    #isStandardUser
    ldap_conn.search('OU=Salus USERS,DC=ad,DC=salus,DC=edu', '(&(objectCategory=user)(memberOf=CN=EIStandard,OU=Salus GROUPS,DC=ad,DC=salus,DC=edu)(sAMAccountName=' + username + '))')
    if len(ldap_conn.entries) < 1:
        print('User does not have standard access.')
    else:
        print('User has standard access.')
    