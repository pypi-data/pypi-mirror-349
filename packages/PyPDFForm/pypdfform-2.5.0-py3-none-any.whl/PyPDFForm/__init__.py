# -*- coding: utf-8 -*-
"""PyPDFForm package for PDF form filling and manipulation.

This package provides tools for filling PDF forms, drawing text and images,
and manipulating PDF form elements programmatically.
"""

__version__ = "2.5.0"

from .wrapper import FormWrapper, PdfWrapper

__all__ = ["FormWrapper", "PdfWrapper"]
