<h1 align="center">
    Meta-Chunking: Learning Text Segmentation and Semantic Completion via Logical Perception
</h1>
<p align="center">
    <a href="https://arxiv.org/abs/2410.12788">
        <img alt="arXiv Paper" src="https://img.shields.io/badge/arXiv-Paper-b31b1b.svg?logo=arxiv">
    </a>
    <a href="https://huggingface.co/papers/2410.12788">
        <img alt="Hugging Face Daily Papers" src="https://img.shields.io/badge/Hugging_Face-Paper.svg?logo=huggingface">
    </a>
    <a href="https://opensource.org/license/apache-2-0">
        <img alt="Apache 2.0 License" src="https://img.shields.io/badge/License-Apache_2.0-4285f4.svg?logo=apache">
    </a>
</p>

**Meta-Chunking** leverages the capabilities of LLMs to flexibly partition documents into logically coherent, independent chunks. Our approach is grounded in a core principle: allowing variability in chunk size to more effectively capture and maintain the logical integrity of content. This dynamic adjustment of granularity ensures that each segmented chunk contains a complete and independent expression of ideas, thereby avoiding breaks in the logical chain during the segmentation process. This not only enhances the relevance of document retrieval but also improves content clarity.

> **Note:** Perplexity is a metric used to measure a language model's ability to predict text. It reflects the degree of uncertainty in generating the next token or sentence given a specific context. Our initial intuition is also to ensure that, during chunking, we split the text at points of certainty and keep it intact at points of uncertainty. This approach is more beneficial for subsequent retrieval and generation. Therefore, in fact, perplexity-based chunking leverages the hallucinations of language models to perceive text boundaries (relative to the boundaries of models), thereby ensuring that chunks are not split at points where language models hallucinate, avoiding the introduction of more hallucinations during retrieval and question answering by LLMs.

## Todo

**We intend to develop this project into a plug-and-play chunking library that incorporates various cutting-edge chunking strategies for LLMs**. While you can use Llama_index for traditional chunking methods, it may be difficult for this library to keep up with the latest chunking technologies. Therefore, we will regularly reconstruct methods from excellent chunking papers into interfaces and add them to the library, making it easier for your system to integrate advanced chunking strategies.

> Currently, all methods are maintained in the **tools** folder. The **eval.ipynb** file demonstrates usage examples of different chunking method interfaces, while each of the other files represents a specific LLMs chunking method.

- [x] Release PPL Chunking and Margin Sampling Chunking
- [x] 1. Refactor methods in Meta-Chunking into several interface formats for easy invocation.
    - [x] PPL Chunking: Strategically introduce the KV caching mechanism to achieve PPL Chunking for both short and long documents (🚀 A Swift and Accurate Text Chunking Technique🌟). 
    - [x] Margin Sampling Chunking: A binary classification judgment is made on whether consecutive sentences need to be segmented, based on the probability obtained through margin sampling to make decisions.
    - [x] Dynamic combination: To accommodate diverse chunking requirements, a strategy of dynamic combination is introduced to assist in chunking, achieving a balance between fine-grained and coarse-grained text chunking.
- [x] 2. Integrating [LumberChunker](https://github.com/joaodsmarques/LumberChunker): Refactoring it into an interface for convenient invocation; combining it with our margin sampling method to overcome the limitation of the original project's inability to use local small models.
- [x] 3. Integrating [Dense X Retrieval](https://github.com/chentong0/factoid-wiki): Refactoring it into an interface for convenient invocation.
- [ ] ......
- [ ] Our follow-up work


## Highlights

- Introduces the concept of Meta-Chunk, which operates at a granularity between sentences and paragraphs.

- Propose two implementation strategies: Margin Sampling (MSP) Chunking and Perplexity (PPL) Chunking.

- Put forward a Meta-Chunk with dynamic combination strategy designed to achieve a valid balance between fine-grained and coarse-grained text segmentation.

