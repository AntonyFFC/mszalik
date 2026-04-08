import os
from mergea5toa4 import merge_fixed_rotation
from mergea5toa4 import merge_two_pages

def prepare_papers(number_of_pages):
    pages = number_of_pages
    number_of_papers = int(pages / 4)
    if pages % 4 != 0:
        number_of_papers += 1
    papers = []
    empty_pages = (number_of_papers * 4) - pages
    b = 1
    e = pages + empty_pages
    for page in range(number_of_papers):
        current_paper = {"BL": b, "L": b + 1 , "R": e -1, "BR": e}
        papers.append(current_paper)
        b += 2
        e -= 2
    if empty_pages == 1:
        papers[0]["BR"] = None
    elif empty_pages == 2:
        papers[0]["BR"] = None
        papers[0]["R"] = None
    elif empty_pages == 3:
        papers[0]["BR"] = None
        papers[0]["R"] = None
        if pages == 1:
            papers[0]["L"] = None
        else:
            papers[1]["BR"] = None
    return papers

number_of_pages = 1
while True:
    if not os.path.exists("{}.html".format(number_of_pages)):
        number_of_pages -= 1
        break
    number_of_pages += 1

merged = 1
created = []
for paper in prepare_papers(number_of_pages):
    l = paper["L"]
    r = paper["R"]
    br = paper["BR"]
    bl = paper["BL"]
    merge_fixed_rotation(f"{br}.pdf", f"{bl}.pdf", f"{br}{bl}.pdf")
    merge_fixed_rotation(f"{l}.pdf", f"{r}.pdf", f"{l}{r}.pdf")
    merge_two_pages(f"{br}{bl}.pdf",
                    f"{l}{r}.pdf",
                    f"sheet_{br}{bl}{l}{r}.pdf")
    created.append(f"sheet_{br}{bl}{l}{r}.pdf")
    merged += 2
fff =["<html><body style='font-family:sans-serif; text-align:center; padding:50px;'><p>Sheet to print: <a href='{}' style='font-size:20px;'>{}</a></p>".format(f,f) for f in created]
print("<html><body style='font-family:sans-serif; text-align:center; padding:50px;'><h1>PDF Generated Successfully</h1><p>All pages: <a href='missale_ready.pdf' style='font-size:20px;'>missale_ready.pdf</a></p>{}</body></html>".format("".join(fff)))
