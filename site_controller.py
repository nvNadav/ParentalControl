
class SiteController:
    def __init__(self):
        self.blocked_sites = []
        self.path = r"C:\Windows\System32\drivers\etc\hosts"
        self.redirect ="127.0.0.1"

    def block(self, site):
        try:
            if site not in self.blocked_sites:
                self.blocked_sites.append(site)
                with open (self.path, 'a') as hostsfile:
                    hostsfile.write(self.redirect + " " + site + "\n")
        except Exception as e:
            print (e)

    def unblock(self, site):
        if site in self.blocked_sites:
            self.blocked_sites.remove(site)
        with open (self.path, 'r') as hostsfile:
            lines = hostsfile.readlines()
        with open (self.path, 'w') as hostsfile:
            for line in lines:
                if not line.strip().endswith(site):
                    hostsfile.write(line)

    def unblock_all(self):
        for site in list(self.blocked_sites):
            self.unblock(site)