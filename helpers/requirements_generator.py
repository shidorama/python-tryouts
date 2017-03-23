import pip
distros = pip.get_installed_distributions()
newlist = { x.project_name : x.version for x in distros}
filecontent = ''
with open('requirements.txt', 'r') as fp:
    filecontent = fp.readlines()
reqs = {}
for line in filecontent:
    x=line[:-1].split('==')
    if len(x) == 2:
        reqs[x[0]] = x[1]
diff = {}
for key, val in reqs.iteritems():
    if newlist.get(key) != val and newlist.get(key):
        diff[key] = newlist.get(key)

# for key, val in newlist.iteritems():
#     if key not in reqs:
#         diff[key] = val
for mod, ver in diff.iteritems():
    print("%s==%s" % (mod, ver))
# print diff
# return