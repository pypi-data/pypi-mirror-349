# RRT’s Pygments style

Reuben Thomas <rrt@sc3d.org>  

This is a simple colourful style for the syntax highlighter [Pygments](https://pygments.org).

It is distributed under a BSD license (see LICENSE file).

It is available in the Pygments distribution as style `rrt`, so most users
will not need to install it separately; this package exists purely for users
wanting to install a newer version of the style than they have access to
with Pygments.


## Installation

The easiest way to install is from PyPI, the Python Package Index:

`pip install pygments-style-rrt-latest`

This will install Pygments itself if you don’t already have it installed.


## Usage

To run Pygments with the `rrt-latest` style:

`pygmentize -S rrt-latest FILE`
