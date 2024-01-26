#include <stdio.h> 
#include <dirent.h> 

int main(void) 
{ 
  struct dirent *de; // Pointer for directory entry 

  // opendir() returns a pointer of DIR type.
    char dir_address[100];
    struct dirent* files[100] = {NULL};
    struct dirent* directories[100] = {NULL};
    int files_index = 0;
    int dir_index = 0;
    printf("enter");
    scanf("%s", dir_address);
  DIR *dr = opendir(dir_address); 


  if (dr == NULL) // opendir returns NULL if couldn't open directory 
  { 
    printf("Could not open current directory" ); 
    return 0; 
  } 

  // Refer http://pubs.opengroup.org/onlinepubs/7990989775/xsh/readdir.html 
  // for readdir() 
  while ((de = readdir(dr)) != NULL)
            if(isDir(de)) {
                directories[dir_index] = de;
                dir_index++;
            } else {
                files[files_index] = de;
                files_index++;
            }
      printf("%s\n", de->d_name);


  closedir(dr);   
  return 0; 
}

