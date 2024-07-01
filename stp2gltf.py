import os

from OCC.Core.TDocStd import TDocStd_Document
from OCC.Core.TCollection import (
    TCollection_AsciiString,
    TCollection_ExtendedString
)
from OCC.Core.XCAFDoc import (
    XCAFDoc_DocumentTool_ShapeTool,
    XCAFDoc_DocumentTool_LayerTool,
)
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeSphere
from OCC.Core.TColStd import TColStd_IndexedDataMapOfStringString
from OCC.Core.Message import Message_ProgressRange
from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh
from OCC.Core.BRepTools import breptools_Clean
from OCC.Extend.DataExchange import read_step_file

# GLTF export
from OCC.Core.RWGltf import RWGltf_CafWriter, RWGltf_WriterTrsfFormat

# create the shapeto export
#shp = BRepPrimAPI_MakeSphere(60.0).Shape()
filename = "NIST_MTC_CRADA_BOX_REV-D 1.stp"
shp = read_step_file(os.path.join("assets", "models", filename))

# create a document
doc = TDocStd_Document(TCollection_ExtendedString("pythonocc-doc"))
shape_tool = XCAFDoc_DocumentTool_ShapeTool(doc.Main())
layer_tool = XCAFDoc_DocumentTool_LayerTool(doc.Main())

# mesh shape
breptools_Clean(shp)
# Triangulate
msh_algo = BRepMesh_IncrementalMesh(shp, True)
msh_algo.Perform()

sub_shape_label = shape_tool.AddShape(shp)

# GLTF options
a_format = RWGltf_WriterTrsfFormat.RWGltf_WriterTrsfFormat_Compact
force_uv_export = True

# metadata
a_file_info = TColStd_IndexedDataMapOfStringString()
a_file_info.Add(
    TCollection_AsciiString("Authors"), TCollection_AsciiString("pythonocc")
)

#
# Binary export
#
binary = True
binary_rwgltf_writer = RWGltf_CafWriter(TCollection_AsciiString(filename.split('.')[0]+".glb"), binary)
binary_rwgltf_writer.SetTransformationFormat(a_format)
binary_rwgltf_writer.SetForcedUVExport(force_uv_export)
pr = Message_ProgressRange()  # this is required
binary_rwgltf_writer.Perform(doc, a_file_info, pr)

#
# Ascii export
#
binary = False
ascii_rwgltf_writer = RWGltf_CafWriter(TCollection_AsciiString(filename.split('.')[0]+".gltf"), binary)
ascii_rwgltf_writer.SetTransformationFormat(a_format)
ascii_rwgltf_writer.SetForcedUVExport(force_uv_export)
pr = Message_ProgressRange()  # this is required
ascii_rwgltf_writer.Perform(doc, a_file_info, pr)
