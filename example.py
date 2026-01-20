import sys; sys.stdout.reconfigure(encoding='utf-8')
from pmp_manip import init_config, get_default_config, info_api, FRProject, fetch_frontpage, fetch_projects
from pmp_manip.utility import file_exists

init_config(get_default_config())

#frontpage = fetch_frontpage()
#project_ids = [project_meta["id"] for project_meta in frontpage["featured"]]
#print(project_ids)
project_ids = ['0413801085', '9366671966', '3029310207', '1987658125', '8439288966', '4430093340', '8019543757', '3726615842', '0876643039', '6811344681', '4642021346', '8754926608', '2530870530', '9520213281', '9197873566', '6583388193', '7732752565', '5797291239', '3278768077', '2872543417']

#project_buffers, error = fetch_projects(project_ids)
#for project_id, project_buffer in project_buffers.items():
#    with open(f"projects/{project_id}.pmp", "wb") as f:
#        f.write(project_buffer.getvalue())


#for project_id in project_ids:
#    if file_exists(f"projects/{project_id}.pmp"):
#        frproject = FRProject.from_file(f"projects/{project_id}.pmp")
frproject = FRProject.from_file("Projekt.pmp")

#projects, error = FRProject.fetch_by_ids(project_ids)
#print(FRProject.__repr__(projects))
#if error:
#    raise error

#frproject = FRProject.fetch_by_id("0131435715")
##print(frproject)
#print(frproject.extensions, frproject.extension_urls)
#input()
#frproject.add_all_extensions_to_info_api(info_api)
#srproject = frproject.to_second(info_api)
#print(srproject)

