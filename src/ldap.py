import ldap3

class LDAP():
    def __init__(self, username, password):
        self.ip_address = "10.1.2.14"
        self.port = 636
        self.userName = username
        self.userPassword = password
        self.server_url = f"ldaps://{self.ip_address}:{self.port}"
        self.ldapUser = "LDAPUser"
        self.ldapPassword = "S@lus.11"
    
    def runQuery(self, query, searchFilter):
        ldap_conn = ldap3.Connection(
            ldap3.Server(self.server_url),
            user=self.ldapUser,
            password=self.ldapPassword,
            auto_bind=True,
        )
        ldap_conn.search(query, searchFilter)
        return ldap_conn.entries

    def isAuthenticated(self):
        rootDN = 'OU=Salus USERS,DC=ad,DC=salus,DC=edu'
        searchFilter = '(sAMAccountName=' + self.userName + ')'
        returnQuery = self.runQuery(rootDN, searchFilter)
        
        if len(returnQuery) == 0:
            return False
        
        #Format DN to attempt user bind credentials
        string = str(returnQuery[0])
        temp = string.split('-')[0].split(':')
        user_dn = temp[1].strip()

        user_ldap_conn = ldap3.Connection(
            ldap3.Server(self.server_url),
            user=user_dn,
            password=self.userPassword,
            authentication="SIMPLE",
        )

        if not user_ldap_conn.bind(): #If not authenticated
            return False
        return True

    def isAdmin(self):
        rootDN = 'OU=Salus USERS,DC=ad,DC=salus,DC=edu'
        searchFilter = '(&(objectCategory=user)(memberOf=CN=EIAdmin,OU=Salus GROUPS,DC=ad,DC=salus,DC=edu)(sAMAccountName=' + self.userName + '))'
        returnQuery = self.runQuery(rootDN, searchFilter)
        if len(returnQuery) < 1:
            return False
        return True

    def isStandardUser(self):
        rootDN = 'OU=Salus USERS,DC=ad,DC=salus,DC=edu'
        searchFilter = '(&(objectCategory=user)(memberOf=CN=EIStandard,OU=Salus GROUPS,DC=ad,DC=salus,DC=edu)(sAMAccountName=' + self.userName + '))'
        returnQuery = self.runQuery(rootDN, searchFilter)
        if len(returnQuery) < 1:
            return False
        return True