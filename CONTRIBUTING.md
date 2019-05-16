How to Contribute
=================

Getting help
------------
To ask questions about XBee MicroPython go to the [Digi Forum][forum].


Reporting a bug
---------------
The way to report bugs is to use the [GitHub issue tracker][issues]. Before
reporting a bug, please read the following points:

1. Make sure that is really a bug by checking the [documentation][doc] and
   consulting the **Which features apply to my device?** section.
2. If you still think you have found a bug, make sure someone has not already
   reported it. See the list of [known issues][issues].
3. If it has not been reported yet, create a new issue. Make sure to add enough
   detail so that the bug can be reproduced.

**Note**: The issue tracker is for bugs, not requests for help. Questions
should be asked on the [Digi Forum][forum] instead.


Suggesting a new feature
------------------------
1. Consult the **Which features apply to my device?** section of the
   [documentation][doc] to ensure that the behavior you would like is not
   excluded in your device.
2. Make sure someone has not already requested it. See the list of
   [known issues][issues].
3. Submit your request in the issue tracker.


Contributing code
-----------------
1. Fork the [XBee MicroPython][xbee-micropython] repository
   ([how to fork a repo][fork-repo]).
2. Create a branch for your contribution. Use a name that defines the purpose
   of the additions/modifications.
3. Make your changes following the code style used in the samples. If you
   are adding a new sample or library, follow the steps described in the
   [Contributing a new sample](#contributing-a-new-sample) and
   [Contributing a new library](#contributing-a-new-library) guides.
4. Execute your code and verify the new functionality or fix works properly.
5. Submit a pull request ([how to create a pull request][pull-request]).

A project developer will review your work and then merge your request into the
project, or come back to you with comments and/or questions.

### Contributing a new sample

XBee MicroPython samples are located in the `samples/` directory of the
repository's root path. Samples are organized in categories, which are 
directories that group samples by functionality.

You can create and nest categories as needed, but before doing so, make sure
there is not already a category that meets your needs.

#### Sample contents

* A sample requires a directory with the sample ID as name. This ID must be a
  short name describing the example purpose, in lowercase and without blank
  spaces. 
* Each sample must include at least the following files inside its directory:
  * `README.md` This file describes the sample functionality, requirements,
    setup, etc. and is used by the **XBee MicroPython plugin for PyCharm**
    to list the sample in the import samples wizard. For that reason, it must
    have a specific structure with required sections. You can copy and modify
    file [README_TEMPLATE.md](samples/README_TEMPLATE.md) from `samples/`
    directory for reference. Notice that lines starting with `>` should be
    removed from the readme file.
  * `main.py` This file contains the source code of the sample and its name
    cannot be changed. See other existing examples and follow the same code
    style to write yours.
* Other directories or files (source code or not) can be added to the sample
  as needed.
    
### Contributing a new library

XBee MicroPython libraries are located in the `lib/` directory of the
repository's root path. libraries are organized in categories, which are 
directories that group them by functionality.

You can create and nest categories as needed, but before doing so, make sure
there is not already a category that meets your needs.

#### Library contents

* A library requires a directory with the library ID as name. The name of the
  directory must be a short name describing the example purpose, in lowercase
  and without blank spaces.
* Each library must include at least the following files inside its directory:
  * `README.md` This file describes the library functionality and requirements
    and is used by the **XBee MicroPython plugin for PyCharm** to list the
    library when creating a new project. For that reason, it must have a
    specific structure with required sections. You can copy and modify file
    [README_TEMPLATE.md](lib/README_TEMPLATE.md) from `lib/` directory for
    reference. Notice that lines starting with `>` should be removed from the
    readme file.
  * `<lib_id>.py` This is the source code file of the library. The name of this
    file is must be the ID of the library unless it is structured as a package
    instead of a module. If the content of the library is a copy or
    modification of an existing module from a third, make sure you add the
    corresponding copyright in the header of the source file.


[doc]: https://www.digi.com/resources/documentation/digidocs/90002219
[forum]: http://www.digi.com/support/forum
[issues]: http://github.com/digidotcom/xbee-micropython/issues
[xbee-micropython]: http://github.com/digidotcom/xbee-micropython
[fork-repo]: https://help.github.com/articles/fork-a-repo/
[pull-request]: https://help.github.com/articles/fork-a-repo/#next-steps