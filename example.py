from pmp_manip import init_config, get_default_config, FRProject

init_config(get_default_config())

frproject = FRProject.fetch_by_id("0131435715")
print(frproject)

# TODO: add tests for project_api
