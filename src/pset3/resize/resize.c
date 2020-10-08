#include <stdio.h>
#include <stdlib.h>

#include "../../../lib/cs50.h"
#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: resize n infile outfile\n");
        return 1;
    }

    //get the factor
    double n = atof(argv[1]);
    if (n < 0 || n > 100)
    {
        printf("Usage: ./resize n infile outfile\n");
        return 1;
    }

    // remember filenames
    char *infile = argv[2];
    char *outfile = argv[3];

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }

    // new width and heigth of outfile's
    int oldWidth = bi.biWidth, oldHeight = bi.biHeight;
    bi.biWidth *= n;
    bi.biHeight *= n;

    // determine padding of new lines
    int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    int oldPadding = (4 - (oldWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    // new size of file
    bi.biSizeImage = ((bi.biWidth * sizeof(RGBTRIPLE)) + padding) * abs(bi.biHeight);
    bf.bfSize = bi.biSizeImage + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);

    // write outfile's BITMAPFILEHEADER
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);

    bool makeSmall = n < 1;
    int a = makeSmall ? 1 / n : 1;

    RGBTRIPLE scan[bi.biWidth];

    // iterate over infile's scanlines
    for (int i = 0, biHeight = abs(oldHeight); i < biHeight; i++)
    {

        int cursor = 0;
        bool writeLine = makeSmall == false || i == 0 || i % a == 0;

        // iterate over pixels in scanline
        for (int j = 0; j < oldWidth; j++)
        {
            // temporary storage
            RGBTRIPLE triple;

            // read RGB triple from infile
            fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

            // write RGB triple to outfile
            if (writeLine && (j == 0 || j % a == 0))
                for (int k = 0; k < n; k++)
                {
                    if (makeSmall)
                        fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
                    else
                    {
                        scan[cursor].rgbtRed = triple.rgbtRed;
                        scan[cursor].rgbtGreen = triple.rgbtGreen;
                        scan[cursor].rgbtBlue = triple.rgbtBlue;
                        cursor++;
                        printf("R: %i, G: %i, B: %i\n", triple.rgbtBlue, triple.rgbtGreen, triple.rgbtBlue);
                    }
                }
        }

        if (!makeSmall)
        {
            for (int l = 0; l < n; l++)
            {
                for (int m = 0; m < bi.biWidth; m++)
                    fwrite(&scan[m], sizeof(RGBTRIPLE), 1, outptr);

                for (int k = 0; k < padding; k++)
                    fputc(0x00, outptr);
            }
        }
        // skip over padding, if any
        fseek(inptr, oldPadding, SEEK_CUR);

        // then add it back (to demonstrate how)
        if (makeSmall && writeLine)
            for (int k = 0; k < padding; k++)
                fputc(0x00, outptr);
    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
