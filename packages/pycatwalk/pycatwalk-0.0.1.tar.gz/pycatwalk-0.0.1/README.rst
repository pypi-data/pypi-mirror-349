Catwalk: An Elegant Framework for Cross-Platform AI Model Execution
==================================================================

Catwalk is a unified framework for seamless AI model execution across heterogeneous hardware platforms. It addresses the growing complexity of model deployment by providing automatic device selection, intelligent caching, and performance optimization while maintaining a simple, elegant API.

Features
--------

- Automatic device detection and optimal selection
- Intelligent model caching with configurable policies
- Hardware-specific performance optimizations
- Unified API across different model formats
- Zero-configuration deployment for most use cases

Installation
-----------

.. code-block:: bash

    pip install pycatwalk

For specific features, you can install optional dependencies:

.. code-block:: bash

    pip install pycatwalk[torch]     # PyTorch support
    pip install pycatwalk[onnx]      # ONNX support
    pip install pycatwalk[huggingface]  # HuggingFace support
    pip install pycatwalk[all]       # All optional dependencies

Quick Start
----------

.. code-block:: python

    from pycatwalk import CatwalkRunner

    # Load and run model with zero configuration
    runner = CatwalkRunner("resnet50.pt")
    results = runner.predict(image_batch)

Advanced Configuration
--------------------

.. code-block:: python

    from pycatwalk import CatwalkRunner, ModelConfig

    config = ModelConfig(
        use_mixed_precision=True,
        enable_compilation=True,
        cache_model=True,
        cache_ttl_hours=48
    )

    runner = CatwalkRunner("bert-base.pt", config=config)
    results = runner.predict(text_tokens)

Links
-----

- Documentation: https://pycatwalk.readthedocs.io/
- Source Code: https://github.com/yourusername/pycatwalk
- Issue Tracker: https://github.com/yourusername/pycatwalk/issues
