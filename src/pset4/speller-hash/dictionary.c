// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "dictionary.h"

// Represents number of buckets in a hash table
#define N 26

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// Represents a hash table
node *hashtable[N];
unsigned int hashTableSize;

// Hashes word to a number between 0 and 25, inclusive, based on its first letter
unsigned int hash(const char *word)
{
    return tolower(word[0]) - 'a';
}

// Adds a new node in hashtable
bool add(node *hTable[], char word[])
{
    // Get hash of word
    unsigned int wordHash = hash(word);

    // Check word length
    if (strlen(word) > (LENGTH + 1))
        return false;

    // Get hash linked list
    node *newNode = (node *)malloc(sizeof(node));

    // If malloc fail
    if (!newNode)
        return false;

    // Copy the word in newNode
    newNode->next = NULL;
    strcpy(newNode->word, word);

    // If new node is first node set up first node
    if (!hashtable[wordHash])
        hashtable[wordHash] = newNode;
    // Else add new node first element
    else
    {
        newNode->next = hashtable[wordHash];
        hashtable[wordHash] = newNode;
    }

    // Return success result
    return true;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Initialize hash table
    for (int i = 0; i < N; i++)
    {
        hashtable[i] = NULL;
    }

    // Open dictionary
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        unload();
        return false;
    }

    // Buffer for a word
    char word[LENGTH + 1];

    // Insert words into hash table
    while (fscanf(file, "%s", word) != EOF)
        if (!add(hashtable, word))
        {
            unload();
            return false;
        }
        else
            hashTableSize++;

    // Close dictionary
    fclose(file);

    // Indicate success
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return hashTableSize;
}

// Finds word in node
bool find(node *targetNode, const char *word)
{
    // Return success result if targetNode->word equals word
    if (strcmp(targetNode->word, word) == 0)
        return true;
    // Find in next node if next node is exists
    else if (targetNode->next != NULL)
        return find(targetNode->next, word);
    // Return not found result
    else
        return false;
}

// Create new char* to str lower chars
void toLower(char *str)
{
    // Convert str chars to lower
    for (int i = 0; str[i] != '\0'; i++)
        if (isalpha(str[i]) && isupper(str[i]))
            str[i] = tolower(str[i]);
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // Copy to word
    char target[LENGTH + 1];
    strcpy(target, word);
    toLower(target);

    // Get hash code of word
    unsigned int hashCode = hash(word);

    // Check target node and return the if the target is exists in the hash table return true 1 else return false 0
    bool result = false;
    if (hashtable[hashCode] != NULL)
        result = find(hashtable[hashCode], target);
    else
        result = false;

    // Return result
    return result;
}

// Frees memory of node
bool freeNode(node *nd)
{
    // Frees the next node
    if (nd->next != NULL)
        if (freeNode(nd->next) == false)
            return false;

    // Frees the node
    free(nd);

    // Return success result
    return true;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // Frees all nodes
    for (int i = 0; i < N; i++)
        if (hashtable[i] != NULL)
            freeNode(hashtable[i]);

    // Return success
    return true;
}
