---
name: chromy
description: This skill provides access to a RAG-like context enhancer that uses Chromadb locally.
---

# Chromy

Whenever the user asks to "use chromy", you should invoke `chromy`, which is a cli tool to perform RAG search.
The tool should be available in the `$PATH` as `chromy`.

You have access to these commands:

- `$ chromy lc` -> Lists the existing collections.
- `$ chromy q <collection> <query>` -> Performs a query. Be sure to quote the `<query>` if this is composed by multiple words.

Then use the response from Chromy to enhance the context and give the user a refined response.

## A note on file sources

The Chromy response returns the metadatas for the chunks it finds. Among these metadatas, there is `file_name`, which refers to the original file that was chunked and imported. **DO NOT ATTEMPT** to find or fetch these files. They most likely do not exist in the filesystem. You **SHOULD ALWAYS** however cite correctly from which files (**ONLY** from Chromy's metadatas) the information is coming.

## Example use case

**START**

User query:

> Search in Chromy information about lovecraft's Dunwich horror.

Step 1: Get the available collections with `chromy lc`. The output is:

```
lovecraft
documents
```

Most likely our information is in the `lovecraft` collection. We will use that for the query.

Step 2: Query using `chromy q lovecraft <query>`. The query _is up to you_, create one keeping into account that this is a raw query on a vector DB. Be concise, extract keywords, avoid noise.

Step 3: Get the results, enhance the context, and respond to the user.

**END**
