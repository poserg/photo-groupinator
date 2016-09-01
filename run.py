#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Run a test server.
from webapp import app
app.run(host='0.0.0.0', port=8080, debug=True)
