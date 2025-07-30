Welcome to local_llm_kit's documentation!
=====================================

``local_llm_kit`` is a Python package that provides an OpenAI-like interface for local language models. It allows you to run language models locally while maintaining compatibility with OpenAI's API structure.

.. toctree::
   :maxdepth: 2
   :caption: Getting Started:

   installation
   quickstart
   tutorials

.. toctree::
   :maxdepth: 2
   :caption: User Guide:

   models
   api_reference
   examples
   best_practices

.. toctree::
   :maxdepth: 2
   :caption: Advanced Topics:

   custom_models
   performance
   troubleshooting

.. toctree::
   :maxdepth: 2
   :caption: Development:

   contributing
   changelog

Features
--------

* OpenAI-compatible API interface
* Support for multiple model backends (Transformers, llama.cpp)
* Chat completion API
* Function calling capability
* Streaming responses
* JSON mode output
* Memory management
* Custom prompt formatting
* Extensive documentation and tutorials
* Performance optimization guides
* Community-driven development

Quick Installation
-----------------

.. code-block:: bash

   pip install local-llm-kit

Quick Example
------------

.. code-block:: python

   from local_llm_kit import LLMClient
   
   # Initialize the client
   client = LLMClient(model="llama2")
   
   # Chat completion
   response = client.chat.completions.create(
       model="llama2",
       messages=[
           {"role": "user", "content": "What is the capital of France?"}
       ]
   )
   
   print(response.choices[0].message.content)

Getting Help
-----------

If you need help using ``local_llm_kit``, you have several options:

1. Check the :doc:`tutorials` for step-by-step guides
2. Read the :doc:`api_reference` for detailed API documentation
3. Look through :doc:`examples` for common use cases
4. Visit our `GitHub Issues <https://github.com/1Utkarsh1/local_llm_kit/issues>`_ page
5. Join our community discussions

Contributing
-----------

We welcome contributions! Please see our :doc:`contributing` guide for details on how to:

* Report bugs
* Suggest features
* Submit pull requests
* Improve documentation

License
-------

``local_llm_kit`` is released under the MIT License. See the LICENSE file for more details.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search` 