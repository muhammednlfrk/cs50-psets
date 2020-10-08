// Definitions
#define BLOCK_SIZE 512

// Library includes
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

// Defines the byte type
typedef unsigned char BYTE;

// Defines a block of FAT file system
typedef BYTE BLOCK[BLOCK_SIZE];

// Local functions
int checkstrend(char *filepath, char *format);

// Initialize point of program
int main(int argc, char *argv[])
{
    // Check arguments
    if (argc != 2 || checkstrend(argv[1], ".raw") == 0)
    {
        fprintf(stderr, "Usage: ./recover [image]\n");
        return 1;
    }

    // Open the file
    FILE *image_file = fopen(argv[1], "r");

    // Return 2 if image file can not open
    if (image_file == NULL)
    {
        fclose(image_file);
        fprintf(stderr, "Image file can not open\n");
        return 2;
    }

    // Read the file if file is not end of file
    BLOCK block;
    FILE *jpegfile = NULL;
    char jpegfilename[20];
    int jpegfilecounter = 0;
    do
    {
        // Read a block
        size_t readsize = fread(&block, sizeof(BLOCK), 1, image_file);

        // Check read size
        if (readsize == 0)
            continue;

        // Create jpeg file if first 4 byte is jpeg format
        if (block[0] == 0xff && block[1] == 0xd8 && block[2] == 0xff && (block[3] & 0xf0) == 0xe0)
        {
            // Close file if file alredy open
            if (jpegfile != NULL)
            {
                fclose(jpegfile);
                jpegfile = NULL;
            }

            // Open and write block in jpg file
            sprintf(jpegfilename, "%03i.jpg", jpegfilecounter);
            jpegfile = fopen(jpegfilename, "w");
            fwrite(block, sizeof(BLOCK), 1, jpegfile);
            jpegfilecounter++;
        }
        // Add bytes in jpeg file if jpeg file is open
        else if (jpegfile != NULL)
            fwrite(block, sizeof(BLOCK), 1, jpegfile);
    } while (!feof(image_file));

    // Close files
    fclose(jpegfile);
    fclose(image_file);

    // Return success result
    return 0;
}

// Checks file format
int checkstrend(char str[], char end[])
{
    for (int i = strlen(str) - 1, j = strlen(end) - 1; i >= 0 && j >= 0; i--, j--)
        if (str[i] != end[j])
            return 0;
    return 1;
}