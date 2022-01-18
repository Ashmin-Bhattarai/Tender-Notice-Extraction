import os
import fitz
try:
    os.mkdir("./Newspapers/")
except FileExistsError:
    pass

try:
    os.mkdir("./Images")
except FileExistsError:
    pass

newspapers=os.listdir("./Newspapers/")
no_of_newspapers=len(newspapers)
newspaper_count=0
for newspaper in newspapers:
    newspaper_count+=1
    print("Processing newspaper: %s ===================[%s/%s]"%(newspaper,newspaper_count,no_of_newspapers))
    if newspaper.endswith(".pdf"):

        doc = fitz.open(os.path.join("./Newspapers/",newspaper))  
        try:
            output_path="./Images/"+newspaper[:-4]+"/"
            os.mkdir(output_path)
        except FileExistsError:
            pass          
        for i in range (0,doc.page_count):
            page=doc.load_page(i)
            pix = page.get_pixmap(matrix=fitz.Matrix(5,5))
            output = "page"+str(i)+".jpg"
            print("\t==>Image conversion of page [%s/%s]"%(i+1,doc.page_count))
            pix.save((output_path+output))
        doc.close()