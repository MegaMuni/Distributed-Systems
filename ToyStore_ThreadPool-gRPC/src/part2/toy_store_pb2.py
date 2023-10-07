# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: toy_store.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0ftoy_store.proto\"\"\n\x13ToyStoreSearchQuery\x12\x0b\n\x03toy\x18\x01 \x01(\t\"6\n\x16ToyStoreSearchResponse\x12\r\n\x05price\x18\x02 \x01(\x02\x12\r\n\x05stock\x18\x03 \x01(\x05\"\x1e\n\x0bToyStoreBuy\x12\x0f\n\x07\x62uy_toy\x18\x05 \x01(\t\"$\n\x13ToyStoreBuyResponse\x12\r\n\x05value\x18\x06 \x01(\x05\x32u\n\x08ToyStore\x12\x38\n\x05Query\x12\x14.ToyStoreSearchQuery\x1a\x17.ToyStoreSearchResponse\"\x00\x12/\n\x07\x42uyItem\x12\x0c.ToyStoreBuy\x1a\x14.ToyStoreBuyResponse\"\x00\x62\x06proto3')



_TOYSTORESEARCHQUERY = DESCRIPTOR.message_types_by_name['ToyStoreSearchQuery']
_TOYSTORESEARCHRESPONSE = DESCRIPTOR.message_types_by_name['ToyStoreSearchResponse']
_TOYSTOREBUY = DESCRIPTOR.message_types_by_name['ToyStoreBuy']
_TOYSTOREBUYRESPONSE = DESCRIPTOR.message_types_by_name['ToyStoreBuyResponse']
ToyStoreSearchQuery = _reflection.GeneratedProtocolMessageType('ToyStoreSearchQuery', (_message.Message,), {
  'DESCRIPTOR' : _TOYSTORESEARCHQUERY,
  '__module__' : 'toy_store_pb2'
  # @@protoc_insertion_point(class_scope:ToyStoreSearchQuery)
  })
_sym_db.RegisterMessage(ToyStoreSearchQuery)

ToyStoreSearchResponse = _reflection.GeneratedProtocolMessageType('ToyStoreSearchResponse', (_message.Message,), {
  'DESCRIPTOR' : _TOYSTORESEARCHRESPONSE,
  '__module__' : 'toy_store_pb2'
  # @@protoc_insertion_point(class_scope:ToyStoreSearchResponse)
  })
_sym_db.RegisterMessage(ToyStoreSearchResponse)

ToyStoreBuy = _reflection.GeneratedProtocolMessageType('ToyStoreBuy', (_message.Message,), {
  'DESCRIPTOR' : _TOYSTOREBUY,
  '__module__' : 'toy_store_pb2'
  # @@protoc_insertion_point(class_scope:ToyStoreBuy)
  })
_sym_db.RegisterMessage(ToyStoreBuy)

ToyStoreBuyResponse = _reflection.GeneratedProtocolMessageType('ToyStoreBuyResponse', (_message.Message,), {
  'DESCRIPTOR' : _TOYSTOREBUYRESPONSE,
  '__module__' : 'toy_store_pb2'
  # @@protoc_insertion_point(class_scope:ToyStoreBuyResponse)
  })
_sym_db.RegisterMessage(ToyStoreBuyResponse)

_TOYSTORE = DESCRIPTOR.services_by_name['ToyStore']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _TOYSTORESEARCHQUERY._serialized_start=19
  _TOYSTORESEARCHQUERY._serialized_end=53
  _TOYSTORESEARCHRESPONSE._serialized_start=55
  _TOYSTORESEARCHRESPONSE._serialized_end=109
  _TOYSTOREBUY._serialized_start=111
  _TOYSTOREBUY._serialized_end=141
  _TOYSTOREBUYRESPONSE._serialized_start=143
  _TOYSTOREBUYRESPONSE._serialized_end=179
  _TOYSTORE._serialized_start=181
  _TOYSTORE._serialized_end=298
# @@protoc_insertion_point(module_scope)