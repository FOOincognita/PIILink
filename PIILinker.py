"""
    @File: PIILinker.py
    @Author: Archer Simmons, UGTA
    @Contact:
        > 832 <dash> 433 <dash> 2245
        > Archer.Simmons@tamu.edu 
    
    This program renames submission folders 
    from GradeScope such that they contain 
    names in preparation for Compare50 scan. 
"""

from os import listdir, chdir, getcwd, path, mkdir, name as OS, system as sys
from alive_progress import alive_bar # pip install alive-progress
from datetime import datetime as dt

#* Student Dataclass
class Student():
    """
        > NAME: Student's name
        > SID: Student's submission ID
        > CODE: Student's submitted code
    """
    
    
    def __init__(self, first_=None, last_=None, SID_=None, uin_=None, email_=None, section_=None) -> None:
        self.NAME:    str = first_ + " " + last_
        self.SID:     int = int(SID_)
        self.CODE:    str = ""
        self.UIN:     str = uin_
        self.EMAIL:   str = email_
        self.SECTION: str = section_
    
    
    def __repr__(self) -> str:
        return f"{self.NAME} | UIN{self.UIN} | {self.EMAIL} | {self.SECTION if self.SECTION else 'N/A'} | Submission ID: {self.SID}"

#* Submission ID & PII Handler
class FileWrangler():
    """
        > ROOTDIR: Root Directory of Program
        > ARCHIVE: Directory of submissions archive
        > SID_CSV: CSV file with student PII & submission IDs
        > CHECK:   List of filenames to run Compare50 on
        > DATABASE: Dict of submission ID (int) keys corresponding to Student objs 
    """
    
    
    def __init__(self) -> None:
        self.ROOTDIR: str = getcwd()
        self.ARCHIVE: str = "NONE"
        self.SID_CSV: str = "NONE"
        self.STARTER: str = "" #? Holds combined starter code
        
        self.CHECK: list[str] = [] #? Contains Filenames of files to extract from student code
        
        self.DATABASE: dict[int, Student] = {}
        
        
    def __getitem__(self, SID: int) -> Student | None:
        """ Returns student given submissionID """
        return self.DATABASE.get(SID)
    
    
    def setup(self) -> None:
        """ Initializes config variables using auto-detection """
        with alive_bar(1) as bar:
            print("Auto-Dectecting Files...")
            
            #* Auto-Detecting Files
            for file in listdir():
                if (fStrp := file.strip()).startswith("Archive_"):
                    self.ARCHIVE = path.join(self.ROOTDIR, fStrp)
                    
                elif fStrp.strip().startswith("SID_") and fStrp.endswith(".csv"):
                    self.SID_CSV = fStrp
                    
            #* Grabbing names of starter code files to extract from student submissions
            try:
                chdir(path.join(self.ROOTDIR, "Starter")) #> Opening starter
                self.CHECK = [file for file in listdir() if file.endswith(".cpp") or file.endswith(".h")]
                if not self.CHECK:
                    print("[ERROR S1]: No .cpp nor .h files found in directory 'Starter'\nEXITING...")
                    exit()
                
                #* Create combined starter code file 
                
                for sFile in self.CHECK:
                    with open(sFile, 'r') as rFile:
                        self.STARTER += f"/* ----- {sFile} | STARTER CODE ----- */\n\n{rFile.read()}"
                    
                chdir(self.ROOTDIR) #> Restoring root directory
                
            except FileNotFoundError: 
                print(f"[ERROR S2]: Missing File in root directory\n\t{self.ROOTDIR}\nEXITING...")
                exit()
            except Exception as e: print(f"[ERROR S3]: Unknown Exception:\n\t{e}")
            bar(1)
    
    
    def build(self) -> None:
        """ Builds student database using exported submission CSV """
        with alive_bar(1) as bar:
            print("Building Student Database...")
        
            #* Building Student Database
            try:
                with open(self.SID_CSV, 'r') as csvFile:
                    csvFile.readline() #? Omit Header
                    self.DATABASE = {
                        int(sid) : Student(first, last, sid, uin, email, section) for sid, first, last, uin, email, section
                            in [
                                [line.split(",")[8]] + line.split(",")[:5]
                                    for line in csvFile.read().split('\n') if "Graded" in line
                            ]
                    } 
                    
            except FileNotFoundError: print(f"[ERROR B1]: {self.SID_CSV} is not in root directory\n\t{self.ROOTDIR}")
            except KeyboardInterrupt: exit()
            except Exception as e: print(f"[ERROR B2]: Unknown Exception:\n\t{e}")
            bar(1)
            print("Database Sucessfully Built...")
       
           
    def extract(self) -> None:
        """ Extracts code from submissions to later write to PII-linked files """
        with alive_bar(len(self.DATABASE)) as bar:
            print("Extracting Student Code...")
            chdir(self.ARCHIVE) #> Open archive directory
            
            #* Iterate over each submission
            for folderName in listdir(): 
                chdir(path.join(self.ARCHIVE, folderName)) #> Open individual folder

                #* Iterate over files listed in CHECK
                for file in self.CHECK:
                    try:
                        with open(file, 'r') as fileCode:
                            #* Store unified code from submitted code file(s) 
                            (stu := self[int(subID := folderName.strip().split('_')[-1])]).CODE \
                                += f"/* ----- {file} | {repr(stu)} ----- */\n\n{fileCode.read()}"
                            
                    except FileNotFoundError: print(f"[WARNING E1]: Missing {file} for:\n\t{self[int(subID)]}")
                    except KeyError: print(f"[ERROR E1]: Missing Key for:\n\t{self[int(subID)]}")
                    except KeyboardInterrupt: exit()
                    except Exception as e: print(f"[ERROR E2]: Unknown Exception:\n\t{e}")
                
                chdir(self.ARCHIVE) #> Restore Archive Directory
                bar(1)
            chdir(self.ROOTDIR) #> Restore Root Directory
            print("Code Extracted & Linked...")
        
        
    def generate(self) -> None:
        """ Generates folder of single files which contain PII-linked code """
        with alive_bar(len(self.DATABASE)) as bar:
            print("Generating PII-Linked Folder...")
            
            #* Create & open unique folder using date & time; created in ROOTDIR
            try:
                T = dt.now()
                fileID = f"{T.year}_{T.second}"
                mkdir(EXPDIR := path.join(self.ROOTDIR, f"PIILinked_{fileID}")) 
                chdir(EXPDIR) #> Open new folder
                
            except KeyboardInterrupt: exit()
            except Exception as e: 
                print(f"[ERROR G1]: Unknown Exception 1:\n\t{e}\nEXITING")
                exit()

            #* Write all files
            try:
                with open("0_STARTER.cpp", 'w') as wFile: #? Write combined starter to directory
                    wFile.write(self.STARTER)
                    
                for subID, student in self.DATABASE.items():
                    with open('_'.join(student.NAME.split()) + '_' + str(subID) + ".cpp", 'w') as wFile:
                        wFile.write(student.CODE)
                    bar(1)
                        
            except KeyboardInterrupt: exit()
            except Exception as e: print(f"[ERROR G2]: Unknown Exception 2:\n\t{e}\nFor: {student.NAME}")
            
            chdir(self.ROOTDIR) #> Restore root directory
            print("Folder Generation Complete...")


    @staticmethod
    def clearTerminal() -> None:
        """ Clears Terminal of All Text """
        sys('cls' if OS == 'nt' else 'clear')
    
    
def main():
    mgr = FileWrangler()
    
    mgr.setup()    #> Setup Params & Data
    mgr.build()    #> Build Student Database
    mgr.extract()  #> Extract Student Code
    mgr.generate() #> Generate PII-Linked Folder of Student Code
    
    print(f"\nSummary:\n\t{len(listdir(mgr.ARCHIVE))} PII-Linked Files Generated")
    
    
if __name__ == "__main__":
    main()
   