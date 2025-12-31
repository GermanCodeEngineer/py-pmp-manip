from pmp_manip import init_config, get_default_config, info_api, FRProject, fetch_frontpage

init_config(get_default_config())

frontpage = fetch_frontpage()
print(list(frontpage.keys()))
for project_meta in frontpage["featured"]:
    print(project_meta)

#frproject = FRProject.fetch_by_id("0131435715")
##print(frproject)
#print(frproject.extensions, frproject.extension_urls)
#input()
#frproject.add_all_extensions_to_info_api(info_api)
#srproject = frproject.to_second(info_api)
#print(srproject)

