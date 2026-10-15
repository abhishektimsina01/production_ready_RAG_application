A production ready rag application for different documents with proper ingestion with reasonable chunking method, hybrid search, rrf for combining the semantic and bm25, chunks evaluation, generation with proper evaluation like faithfulness etc.\

Production level RAG system:-

- Document
- Parsing and loaded
- Strcutre identify based upn the tyoe of document
- chunker will make the chunks based upon the strcutre preserving the metadata
- embedding
- vectore db
- hybrid search
- generation
- evaluation


the document parser will the parse the document which will protect the structure of the docuemt such that the parsed document will contain multiple parsed documents inside it, separated based upon the strcutre of the docuemtn itself.
For example, the pyPDF parser would parse the document such that each Document object contain the whole one page content including the metadata.

Now, when the chunker need to chunk the documents into reasonable chunks, it can easily perform the chunking process based upon the structure bevasue we can easily identify the strcutrue of the document which we have parsed, through its metadata.
Due to this, the chunks will respect/obey the hiearchy of the document and we can also add the infromation about the parent headings and the path from the heading to the content or paragraph for more contexualized chunk, so that each chunk are not isolated text.

Use the HNSW or ANN(approximate nearest neighbour) index for the faster similarity search. ANN is suggested more as it will find the vector embedding which are closer the the query embedding instead f trying to find the exact embedding.

Semantic search and BM25 search and then combine them using the reciprocal rank fusion (RRF) to find te top best chunks from the two methods after ranking them and then genertation.