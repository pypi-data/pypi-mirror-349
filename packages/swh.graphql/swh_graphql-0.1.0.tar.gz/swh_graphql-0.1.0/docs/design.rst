Design
========

Architecture
------------

- On a high level, a multitier pattern is used

  Schema represents the user facing part, resolvers the controller and backend to fetch data

- `Starlette <https://www.starlette.io/>`_ is used as the application framework
- `Ariadne <https://github.com/mirumee/ariadne>`_, a ``schema first`` python library is used.

  | Ariadne is built on top of `graphql-core <https://github.com/graphql-python/graphql-core>`_.
  | The library is used only for binding resolvers to the schema and for some simple actions like
    static cost calculation.
  | This is not a hard dependency, and can be replaced if needed.

Schema
--------

- Schema is written in `SDL <https://www.apollographql.com/tutorials/lift-off-part1/03-schema-definition-language-sdl>`_.
- Schema is following `relay specifications <https://relay.dev/docs/guides/graphql-server-specification/>`_ using Nodes and Connections.
- Naming: lower Camelcase is used for fields and input arguments, CamelCase for types and enums

Resolvers
---------

| Schema objects are connected to the corresponding objects in `resolvers.resolvers.py <https://gitlab.softwareheritage.org/swh/devel/swh-graphql/-/blob/master/swh/graphql/resolvers/resolvers.py>`_
| Each query returns a resolver object with its attributes matching to the schema.
| Every resolver will accept two args. The parent object (called self.obj in the resolver class) and the client/user inputs (self.kwargs in a resolver class)
| self.obj will be None for a top level (query level entrypoint) resolver.
|
| Mainly there are three types of resolvers. Nodes, Connections and SimpleLists
|

- `Node <https://gitlab.softwareheritage.org/swh/devel/swh-graphql/-/blob/master/swh/graphql/resolvers/base_node.py>`_

  | Inherit ``resolvers.base_node.BaseNode`` to create a node resolver
  | Use this to return a single object
  | eg: Origin
  |
  | override ``_get_node_data`` to return the real data. This can return either an object or a map.
  | override ``_get_node_from_data`` in case you want to format the data before returning.
  |

- `Connection <https://gitlab.softwareheritage.org/swh/devel/swh-graphql/-/blob/master/swh/graphql/resolvers/base_connection.py>`_

  | Inherit ``resolvers.base_connection.BaseConnection`` to create a connection resolver
  | Use this to return a paginated list
  | Pagination response will be automatically created with edges and PageInfo in the response as per by the `relay specification <https://relay.dev/docs/guides/graphql-server-specification/>`_.
  | eg: Origins
  |
  | override ``_get_connection_data`` to return the real data
  | handlers are available to read general user arguments like ``first`` and ``after`` and can be overridden for the specific case.
  |

- `SimpleList <https://gitlab.softwareheritage.org/swh/devel/swh-graphql/-/blob/master/swh/graphql/resolvers/base_connection.py?ref_type=heads#L158>`_

  | Inherit ``resolvers.base_connection.BaseList`` to create a simple list resolver
  | Use this to return a non paginated simple list
  | eg: resolveSWHID (This is returning a simple list, instead of a node, to handle the rare case of SWHID collisions)
  |
  | override ``_get_results`` to return the real data
  |

- Others

  - Binary string

    To return an object with a string and its binary value

  - Date with offset

    To return an object with an isoformat data and its offset as a Binary string

Resolver factory
----------------

| The resolver object for the response is always created at `resolvers.resolver_factory <https://gitlab.softwareheritage.org/swh/devel/swh-graphql/-/blob/master/swh/graphql/resolvers/resolver_factory.py>`_.
| There are different factories for nodes, connections and lists.
|
| In most of the cases the responsible resolver class can be intuitively identified from the factory itself.
| This will save reading the code in ``resolvers.resolvers`` module, which is generally a lot more complex.
| A rough pattern used to name an object is <parent obj>-<child field>
|
| eg: requesting a headbranch inside a snapshot is represented by ``snapshot-headbranch`` key
  and handled by ``SnapshotHeadBranchNode`` class
| or
| key ``revision-parents`` (parents inside a revision) is handled by ``ParentRevisionConnection`` class.
| or
| key ``directory-directoryentry`` (a directory-entry from a directory) is handled by ``DirEntryInDirectoryNode`` class.

Custom Scalars
---------------

A few custom scalars are defined `here <https://gitlab.softwareheritage.org/swh/devel/swh-graphql/-/blob/master/swh/graphql/resolvers/scalars.py>`__.

- SWHID

  Serializer and parser for SWHID

- ID

  A string used as cache key for JS clients

- DateTime

  Serializer for Datetime objects

Targets and union types
------------------------

| A reusable pattern is followed when a target object is referenced.
| An intermediate target type is introduced between the object and the final target node.
| This is useful to get some information about a a target object even if it is missing from the archive.
| This will also save a backend call in case the client is only interested in the target hash and type.
|
| eg pattern
|

.. code-block::

  parentObject {
    ...
    target {
      ...
      type
      SWHID   // This could be any identifier (can be a hash)
      node {  // The real object
        ..
      }
    }
  }


| node field inside a target will be a UNION type in most of the cases.

Errors
------

| Generally the GraphQl server will always return a 200 success irrespective of the response data.
| During validation/parse or query syntax errors, or when it is impossible to generate a response, it will return error statuses.
  (Error 400 for validation and query syntax errors)
|
| An error `formatter <https://gitlab.softwareheritage.org/swh/devel/swh-graphql/-/blob/master/swh/graphql/errors/handlers.py>`_ is used to manage client error messages.

Client errors not reported in Sentry are
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ObjectNotFoundError

  Requested object is missing. Only node resolvers will raise this. (Similar to a 404 error).

- PaginationError

  Issue with pagination arguments, invalid cursor too big first argument etc. This is a validation error.

- InvalidInputError

  Issues like invalid SWHID, or an invalid sort order from a client. This is a validation error.

- QuerySyntaxError

  Error in client query, caught by ariadne while parsing. This is a validation error

Other possible errors (reported in Sentry)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- DataError
- Errors related to authentication
- Unhandled errors

Backends
----------

- Archive

  All the calls to swh-storage

- Search

  All the calls to swh-search

Middlewares
-------------

- LogMiddleware

  Used to send statsd matrices

Local paginations
-----------------

| Local pagination is used in some places where pagination is not supported in the backend.
| This is using index based slices and is generally inefficient. List index is used as the cursor here.
| All the fields/types using local pagination costs extra to execute.
|

eg: DirectoryEntry

| All the local pagination is handled by a utility function called `utils.get_local_paginated_data <https://gitlab.softwareheritage.org/swh/devel/swh-graphql/-/blob/master/swh/graphql/utils/utils.py#L50>`_.
| All the local paginations have a FIXME tag in the code.

Tests
-----

| Test objects for GraphQL tests are created in `tests.tests.data.py <https://gitlab.softwareheritage.org/swh/devel/swh-graphql/-/blob/master/swh/graphql/tests/data.py>`_.
| Functional tests are using starlette `testclient <https://www.starlette.io/testclient/>`_.
| Core functions for the functional tests are in `tests.functional.utils.py <https://gitlab.softwareheritage.org/swh/devel/swh-graphql/-/blob/master/swh/graphql/tests/functional/utils.py>`_.
| A few unit tests are also available.


Add a new Scalar field inside a type
-------------------------------------

- Add the field in the schema
- Add the cost associated. (Ideally this should be 0 for all scalars)
- Find the resolver class from ``resolvers.resolvers.py`` (This step can be skipped in most of the cases by directly checking the factory dict)
- Add a field either in the backend response or as a property in the resolver class.
- If the field involves a new backend call or any extra computing, add it as new type instead of a field. (By following the steps below)

Add a new type field inside another type
------------------------------------------

- Add the type in the schema
- Add a field along with arguments in the parent type connecting to the newly added type.
- Add the cost associated. Multipliers can be used if needed.
- Add the resolver class using the right base class and override the required function/s.
- Add a backend function (if necessary) to fetch data
- Connect the route in ``resolvers.resolvers.py``
- Bind the class in the resolver factory ``resolvers.resolver_factory.py``.
- You have to add the type in the type in `app.py <https://gitlab.softwareheritage.org/swh/devel/swh-graphql/-/blob/master/swh/graphql/app.py>`_, in case you have sub fields to resolve.

- eg: `MR <https://gitlab.softwareheritage.org/swh/devel/swh-graphql/-/merge_requests/168>`_ to add an entry field in the Directory object. It is created as new resolver object as has a cost.

Add a new entrypoint
---------------------

- This is same as adding a new type inside another type. The parent type will be the root (query) in this case.

Cost calculator
---------------

- Static and calculated by ariadne

  | This check is executed before running the query.
  | It may not be a good idea to use this to calculate credits as this always assumes the maximum possible cost of a query.

Client
------

- `GraphiQL <https://github.com/graphql/graphiql/tree/main/packages/graphiql>`_ based and is returned from the GrapQL server itself.

Future works
-------------

- Indexers

  Add an indexer backend

- Metadata

  | Add a metadata backend.
  | The major issue here is it is not well structured. It is not very helpful to return raw json.
  |

- Disable cors

  Cors is enabled for all the domains now. Limit only to legit clients

- More backends

  Graph backend, Provenance backend

- More fields

  | More fields can be added with more backends.
  | Eg: 'firstSeen' field in a content object can be added from provenance
  |

- Mutations

  Write APIs

- Dynamic query cost calculator and partial response

  | To calculate exact query cost.
  | It is also possible to return part of the response depending on the cost.
  |

- Advanced rate limiter

  Maybe as a different service. To support user level query quota and time based restrictions.

- De-couple client and server

  | Client UI is returned by the same service. It is a good idea to make them separate. swh-client is a basic working copy
  | A simple independent client is available `here <https://gitlab.softwareheritage.org/jayeshv/swh-explorer>`_ .
  |

- Make fully relay complaint

  Missing startCursor and itemCursor in pagination. totalCount (not in relay spec) is missing from most of the connections.

- Sentry transactions

  Create a transaction per query and add all the objects.

- Backend/performance improvements by writing new queries with joins

  Write bigger backend queries to avoid multiple storage hits.

- Add type to resolver arguments

  User inputs are not typed now and are available in self.kwargs. Add types to each of the inputs

- Remove local paginations

  Move all the pagination to the backend

- Cache

  Ideally in the storage level.

- Address FIXMEs

  Most of them are related to local pagination

- Make resolvers asynchronous

  Could improve performance in case a query requests multiple types in a single request.
