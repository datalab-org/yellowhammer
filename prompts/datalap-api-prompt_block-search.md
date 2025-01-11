# Preparing prmopt for when datalab block search is implemented in API


Datalab is data management platform. We refer to an instance of datalab as "a datalab". One datalab is typically used to capture experimental data for a single research group. The datalab consists of a database of "items" which have types such as "sample". Each item contains "data blocks" which contain information about the item. Block types are shared across the datalab and described by a JSON schema.

Assume `DATALAB_URL` has been set by an environment variable.

Retrieve the datalab instance URL from the environment variable `DATALAB_URL`.
The datalab Python API can query entries on a datalab instance at this URL.
Each method of the DatalabClient class will return a dictionary constructed directly
from the JSON response of the Datalab API.

Assume `DATALAB_API_KEY` have been set an environment variable.

The rest of this prompt contains the README for the datalab python API module `datalab_api`, which you already have installed.

Python API
This package implements basic functionality for displaying and manipulating entries:

```python
from datalab_api import DatalabClient

with DatalabClient(<DATALAB_URL>) as client:

    # Get the info about this datalab instance
    client.get_info()

    # Get the current user's info
    client.authenticate()

    # Search for items with the string
    items = client.search_items("search-values")

    # List all items of a given type
    # Types can be 'samples' or 'starting_materials'
    items = client.get_items(item_type="samples")

    # Get more info on a particular item called 'test'
    item = client.get_item(item_id="test")

    # Create a new item with some data that matches the corresponding `item_type` schema
    json_data = {"chemform": "NaCl"}
    client.create_item(item_id="test_new", item_type="samples", item_data=json_data)

    # Attach a file to an item and get the uploaded ID
    file_response = client.upload_file(filepath="my_echem_data.mpr", item_id="test")
    file_id = file_response["file_id"]

    # Create a data block for a sample, then show the plot
    client.create_data_block(item_id="test", file_ids=file_id)

    # Download all files attached to a sample and return their paths
    file_paths = client.get_item_files(item_id="test")

    # Get the item graph, useful for finding relationships
    graph = client.get_item_graph()

```

If you are asked to search through data blocks for unlisted information, first use the client.get_block_info() function, which returns a list of block definitions in JSON format. **IMPORTANT: block schemas are defined across the datalab and blocks are contained within samples. Samples are also defined by JSON schemas. Do not confuse blocks and samples.**

Each block has the following structure:
    attributes: Contains key details about the block.
        accepted_file_extensions: Specifies a list of file extensions the block can process. If the block does not support files, this is empty or null.
        description: A brief description of what the block does.
        name: The name of the block, indicating its purpose.
        version: The version number of the block.
    id: A unique identifier for the block.
    type: Specifies the general category or type of the block.

Generic block structure
{
    "attributes": {
        "accepted_file_extensions": [".txt", ".wdf"],
        "description": "Visualize 1D Raman spectroscopy data.",
        "name": "Raman spectroscopy",
        "version": "0.1.0"
    },
    "id": "raman",
    "type": "block_type"
}

How to Use

    Search by Block Type: Filter through blocks by checking the type attribute to identify blocks belonging to a specific category, such as "block_type".
    File Compatibility: Identify which block can process a specific file format by searching within accepted_file_extensions.
    Description and Purpose: To understand the functionality of each block, examine the description attribute.
    Versioning: Note that each block's version attribute can help in identifying if certain features are available based on the block's version.

For instance, if you need a block that supports .txt files for mass spectrometry, you would look for blocks with "accepted_file_extensions": [".txt"] and "name": "Mass spectrometry".

Here is an abridged JSONSchema for a sample, that also has some info about other
types.

```json
{
  "title": "Sample",
  "description": "A model for representing an experimental sample.",
  "type": "object",
  "properties": {
    "blocks_obj": {
      "title": "Blocks Obj",
      "default": {},
      "type": "object"
    },
    "display_order": {
      "title": "Display Order",
      "default": [],
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "collections": {
      "title": "Collections",
      "default": [],
      "type": "array",
      "items": {
        "$ref": "#/definitions/Collection"
      }
    },
    "revision": {
      "title": "Revision",
      "default": 1,
      "type": "integer"
    },
    "revisions": {
      "title": "Revisions",
      "type": "object"
    },
    "creator_ids": {
      "title": "Creator Ids",
      "default": [],
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "creators": {
      "title": "Creators",
      "type": "array",
      "items": {
        "$ref": "#/definitions/Person"
      }
    },
    "type": {
      "title": "Type",
      "default": "samples",
      "const": "samples",
      "pattern": "^samples$",
      "type": "string"
    },
    "immutable_id": {
      "title": "Immutable ID",
      "type": "string"
    },
    "last_modified": {
      "title": "Last Modified",
      "type": "date",
      "format": "date-time"
    },
    "relationships": {
      "title": "Relationships",
      "type": "array",
      "items": {
        "$ref": "#/definitions/TypedRelationship"
      }
    },
    "refcode": {
      "title": "Refcode",
      "minLength": 1,
      "maxLength": 40,
      "pattern": "^[a-z]{2,10}:(?:[a-zA-Z0-9]+|[a-zA-Z0-9][a-zA-Z0-9._-]+[a-zA-Z0-9])$",
      "type": "string"
    },
    "item_id": {
      "title": "Item Id",
      "minLength": 1,
      "maxLength": 40,
      "pattern": "^(?:[a-zA-Z0-9]+|[a-zA-Z0-9][a-zA-Z0-9._-]+[a-zA-Z0-9])$",
      "type": "string"
    },
    "description": {
      "title": "Description",
      "type": "string"
    },
    "date": {
      "title": "Date",
      "type": "date",
      "format": "date-time"
    },
    "name": {
      "title": "Name",
      "type": "string"
    },
    "files": {
      "title": "Files",
      "type": "array",
      "items": {
        "$ref": "#/definitions/File"
      }
    },
    "file_ObjectIds": {
      "title": "File Objectids",
      "default": [],
      "type": "array",
      "items": {
        "type": "string"
      }
    },
    "chemform": {
      "title": "Chemform",
      "example": [
        "Na3P",
        "LiNiO2@C"
      ],
      "type": "string"
    },
    "synthesis_constituents": {
      "title": "Synthesis Constituents",
      "default": [],
      "type": "array",
      "items": {
        "$ref": "#/definitions/Constituent"
      }
    },
    "synthesis_description": {
      "title": "Synthesis Description",
      "type": "string"
    }
  },
  "required": [
    "item_id"
  ],
  "definitions": {
    "KnownType": {
      "title": "KnownType",
      "description": "An enumeration of the types of entry known by this implementation, should be made dynamic in the future.",
      "enum": [
        "samples",
        "starting_materials",
        "blocks",
        "files",
        "people",
        "collections"
      ],
      "type": "string"
    },
    "File": {
      "title": "File",
      "description": "A model for representing a file that has been tracked or uploaded to datalab.",
      "type": "object",
      "properties": {
        "revision": {
          "title": "Revision",
          "default": 1,
          "type": "integer"
        },
        "revisions": {
          "title": "Revisions",
          "type": "object"
        },
        "creator_ids": {
          "title": "Creator Ids",
          "default": [],
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "creators": {
          "title": "Creators",
          "type": "array",
          "items": {
            "$ref": "#/definitions/Person"
          }
        },
        "type": {
          "title": "Type",
          "default": "files",
          "const": "files",
          "pattern": "^files$",
          "type": "string"
        },
        "immutable_id": {
          "title": "Immutable ID",
          "type": "string"
        },
        "last_modified": {
          "title": "Last Modified",
          "type": "date",
          "format": "date-time"
        },
        "relationships": {
          "title": "Relationships",
          "type": "array",
          "items": {
            "$ref": "#/definitions/TypedRelationship"
          }
        },
        "size": {
          "title": "Size",
          "description": "The size of the file on disk in bytes.",
          "type": "integer"
        },
        "last_modified_remote": {
          "title": "Last Modified Remote",
          "description": "The last date/time at which the remote file was modified.",
          "type": "date",
          "format": "date-time"
        },
        "item_ids": {
          "title": "Item Ids",
          "description": "A list of item IDs associated with this file.",
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "blocks": {
          "title": "Blocks",
          "description": "A list of block IDs associated with this file.",
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "name": {
          "title": "Name",
          "description": "The filename on disk.",
          "type": "string"
        },
        "extension": {
          "title": "Extension",
          "description": "The file extension that the file was uploaded with.",
          "type": "string"
        },
        "original_name": {
          "title": "Original Name",
          "description": "The raw filename as uploaded.",
          "type": "string"
        },
        "location": {
          "title": "Location",
          "description": "The location of the file on disk.",
          "type": "string"
        },
        "url_path": {
          "title": "Url Path",
          "description": "The path to a remote file.",
          "type": "string"
        },
        "source": {
          "title": "Source",
          "description": "The source of the file, e.g. 'remote' or 'uploaded'.",
          "type": "string"
        },
        "time_added": {
          "title": "Time Added",
          "description": "The timestamp for the original file upload.",
          "type": "string",
          "format": "date-time"
        },
        "metadata": {
          "title": "Metadata",
          "description": "Any additional metadata.",
          "type": "object"
        },
        "representation": {
          "title": "Representation"
        },
        "source_server_name": {
          "title": "Source Server Name",
          "description": "The server name at which the file is stored.",
          "type": "string"
        },
        "source_path": {
          "title": "Source Path",
          "description": "The path to the file on the remote resource.",
          "type": "string"
        },
        "is_live": {
          "title": "Is Live",
          "description": "Whether or not the file should be watched for future updates.",
          "type": "boolean"
        }
      },
      "required": [
        "item_ids",
        "blocks",
        "name",
        "extension",
        "time_added",
        "is_live"
      ]
    },
    "EntryReference": {
      "title": "EntryReference",
      "description": "A reference to a database entry by ID and type.\n\nCan include additional arbitarary metadata useful for\ninlining the item data.",
      "type": "object",
      "properties": {
        "type": {
          "title": "Type",
          "type": "string"
        },
        "name": {
          "title": "Name",
          "type": "string"
        },
        "immutable_id": {
          "title": "Immutable Id",
          "type": "string"
        },
        "item_id": {
          "title": "Item Id",
          "minLength": 1,
          "maxLength": 40,
          "pattern": "^(?:[a-zA-Z0-9]+|[a-zA-Z0-9][a-zA-Z0-9._-]+[a-zA-Z0-9])$",
          "type": "string"
        },
        "refcode": {
          "title": "Refcode",
          "minLength": 1,
          "maxLength": 40,
          "pattern": "^[a-z]{2,10}:(?:[a-zA-Z0-9]+|[a-zA-Z0-9][a-zA-Z0-9._-]+[a-zA-Z0-9])$",
          "type": "string"
        }
      },
      "required": [
        "type"
      ]
    },
    "InlineSubstance": {
      "title": "InlineSubstance",
      "type": "object",
      "properties": {
        "name": {
          "title": "Name",
          "type": "string"
        },
        "chemform": {
          "title": "Chemform",
          "type": "string"
        }
      },
      "required": [
        "name"
      ]
    },
    "Constituent": {
      "title": "Constituent",
      "description": "A constituent of a sample.",
      "type": "object",
      "properties": {
        "item": {
          "title": "Item",
          "anyOf": [
            {
              "$ref": "#/definitions/EntryReference"
            },
            {
              "$ref": "#/definitions/InlineSubstance"
            }
          ]
        },
        "quantity": {
          "title": "Quantity",
          "minimum": 0,
          "type": "number"
        },
        "unit": {
          "title": "Unit",
          "default": "g",
          "type": "string"
        }
      },
      "required": [
        "item",
        "quantity"
      ]
    }
  }
}
```
