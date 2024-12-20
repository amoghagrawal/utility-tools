import bpy
import random

class OBJECT_PT_CustomPanel(bpy.types.Panel):
    bl_label = "Utility Tools"
    bl_idname = "OBJECT_PT_CustomPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tools'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        box = layout.box()
        row = box.row()
        row.prop(scene, "expand_renamer", text="Object Renamer", emboss=False, icon="TRIA_DOWN" if scene.expand_renamer else "TRIA_RIGHT")
        if scene.expand_renamer:
            row = box.row()
            row.prop(scene, "renamer_prefix")
            row.prop(scene, "renamer_suffix")
            box.prop(scene, "renamer_numbering")
            if scene.renamer_numbering:
                box.prop(scene, "renamer_start_number")
            box.operator("object.rename_selected_objects")

        layout.separator()

        box = layout.box()
        row = box.row()
        row.prop(scene, "expand_cleanup", text="Scene Cleanup", emboss=False, icon="TRIA_DOWN" if scene.expand_cleanup else "TRIA_RIGHT")
        if scene.expand_cleanup:
            box.prop(scene, "cleanup_unused_materials")
            box.prop(scene, "cleanup_unused_textures")
            box.prop(scene, "cleanup_unused_meshes")
            box.operator("object.cleanup_scene")

        layout.separator()

        box = layout.box()
        row = box.row()
        row.prop(scene, "expand_export", text="Export Helper", emboss=False, icon="TRIA_DOWN" if scene.expand_export else "TRIA_RIGHT")
        if scene.expand_export:
            box.prop(scene, "export_format")
            box.prop(scene, "export_scope")
            box.prop(scene, "export_apply_modifiers")
            box.prop(scene, "export_include_animation")
            box.prop(scene, "export_embed_textures")
            box.prop(scene, "export_compress")
            box.operator("object.export_helper")

        layout.separator()

        box = layout.box()
        row = box.row()
        row.prop(scene, "expand_hierarchy", text="Hierarchy Organizer", emboss=False, icon="TRIA_DOWN" if scene.expand_hierarchy else "TRIA_RIGHT")
        if scene.expand_hierarchy:
            box.operator("object.organize_hierarchy")
            row = box.row()
            row.prop(scene, "collection_renamer_prefix")
            row.prop(scene, "collection_renamer_suffix")
            box.operator("object.rename_collections")

        layout.separator()

        box = layout.box()
        row = box.row()
        row.prop(scene, "expand_duplicator", text="Object Duplicator", emboss=False, icon="TRIA_DOWN" if scene.expand_duplicator else "TRIA_RIGHT")
        if scene.expand_duplicator:
            box.prop(scene, "duplicate_count")
            box.operator("object.duplicate_objects")

        layout.separator()

        box = layout.box()
        row = box.row()
        row.prop(scene, "expand_aligner", text="Object Aligner", emboss=False, icon="TRIA_DOWN" if scene.expand_aligner else "TRIA_RIGHT")
        if scene.expand_aligner:
            box.prop(scene, "align_axis")
            box.operator("object.align_objects")

        layout.separator()

        box = layout.box()
        row = box.row()
        row.prop(scene, "expand_randomizer", text="Object Randomizer", emboss=False, icon="TRIA_DOWN" if scene.expand_randomizer else "TRIA_RIGHT")
        if scene.expand_randomizer:
            box.prop(scene, "randomize_position")
            box.prop(scene, "randomize_rotation")
            box.prop(scene, "randomize_scale")
            box.operator("object.randomize_objects")

        layout.separator()

        box = layout.box()
        row = box.row()
        row.prop(scene, "expand_colorizer", text="Object Colorizer", emboss=False, icon="TRIA_DOWN" if scene.expand_colorizer else "TRIA_RIGHT")
        if scene.expand_colorizer:
            box.prop(scene, "random_color")
            box.prop(scene, "color")
            box.prop(scene, "color_alpha")
            box.prop(scene, "colorize_scope", text="Scope")
            box.operator("object.colorize_objects")

        layout.separator()

        box = layout.box()
        row = box.row()
        row.prop(scene, "expand_merger", text="Object Merger", emboss=False, icon="TRIA_DOWN" if scene.expand_merger else "TRIA_RIGHT")
        if scene.expand_merger:
            box.operator("object.merge_objects")


class OBJECT_OT_RenameSelectedObjects(bpy.types.Operator):
    bl_idname = "object.rename_selected_objects"
    bl_label = "Rename Selected Objects"

    def execute(self, context):
        prefix = context.scene.renamer_prefix
        suffix = context.scene.renamer_suffix
        numbering = context.scene.renamer_numbering
        start_number = context.scene.renamer_start_number

        for i, obj in enumerate(context.selected_objects):
            name = prefix
            if numbering:
                name += f"{start_number + i:03d}"
            name += suffix
            obj.name = name

        self.report({'INFO'}, "Selected objects renamed successfully.")
        return {'FINISHED'}


class OBJECT_OT_CleanupScene(bpy.types.Operator):
    bl_idname = "object.cleanup_scene"
    bl_label = "Cleanup Scene"

    def execute(self, context):
        removed_materials = removed_textures = removed_meshes = 0

        if context.scene.cleanup_unused_materials:
            removed_materials = self.remove_unused(bpy.data.materials)
        if context.scene.cleanup_unused_textures:
            removed_textures = self.remove_unused(bpy.data.textures)
        if context.scene.cleanup_unused_meshes:
            removed_meshes = self.remove_unused(bpy.data.meshes)

        self.report({'INFO'}, f"Removed {removed_materials} materials, {removed_textures} textures, {removed_meshes} meshes.")
        return {'FINISHED'}

    def remove_unused(self, data_block):
        removed_count = 0
        for item in list(data_block):
            if not item.users:
                data_block.remove(item)
                removed_count += 1
        return removed_count


class OBJECT_OT_ExportHelper(bpy.types.Operator):
    bl_idname = "object.export_helper"
    bl_label = "Export"

    filepath: bpy.props.StringProperty(subtype='FILE_PATH')

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        format = context.scene.export_format
        scope = context.scene.export_scope
        apply_modifiers = context.scene.export_apply_modifiers
        include_animation = context.scene.export_include_animation
        embed_textures = context.scene.export_embed_textures
        compress = context.scene.export_compress

        if format == 'FBX':
            bpy.ops.export_scene.fbx(filepath=self.filepath, 
                                     use_selection=(scope == 'SELECTED'), 
                                     apply_modifiers=apply_modifiers, 
                                     bake_anim=include_animation)
        elif format == 'GLTF':
            bpy.ops.export_scene.gltf(filepath=self.filepath, 
                                      export_selected=(scope == 'SELECTED'), 
                                      export_apply=apply_modifiers, 
                                      export_animations=include_animation,
                                      export_texture_dir="",
                                      export_embed_images=embed_textures)
        elif format == 'OBJ':
            bpy.ops.export_scene.obj(filepath=self.filepath, 
                                     use_selection=(scope == 'SELECTED'), 
                                     use_animation=include_animation)

        self.report({'INFO'}, f"Exported to {self.filepath}")
        return {'FINISHED'}


class OBJECT_OT_OrganizeHierarchy(bpy.types.Operator):
    bl_idname = "object.organize_hierarchy"
    bl_label = "Organize Hierarchy"

    def execute(self, context):
        types = {"MESH": "Meshes", "LIGHT": "Lights", "CAMERA": "Cameras"}
        summary = []

        for obj_type, collection_name in types.items():
            collection = bpy.data.collections.get(collection_name) or bpy.data.collections.new(collection_name)
            if collection.name not in context.scene.collection.children:
                context.scene.collection.children.link(collection)

            count = 0
            for obj in bpy.data.objects:
                if obj.type == obj_type:
                    for coll in obj.users_collection:
                        coll.objects.unlink(obj)

                    if obj.name not in collection.objects:
                        collection.objects.link(obj)
                        count += 1

            summary.append(f"{collection_name}: {count} objects organized.")

        self.report({'INFO'}, f"Hierarchy Organized:\n{chr(10).join(summary)}")
        return {'FINISHED'}


class OBJECT_OT_RenameCollections(bpy.types.Operator):
    bl_idname = "object.rename_collections"
    bl_label = "Rename Collections"

    def execute(self, context):
        prefix = context.scene.collection_renamer_prefix
        suffix = context.scene.collection_renamer_suffix

        for collection in bpy.data.collections:
            name = prefix + collection.name + suffix
            collection.name = name

        self.report({'INFO'}, "Collections renamed successfully.")
        return {'FINISHED'}


class OBJECT_OT_DuplicateObjects(bpy.types.Operator):
    bl_idname = "object.duplicate_objects"
    bl_label = "Duplicate Objects"

    def execute(self, context):
        count = context.scene.duplicate_count
        for _ in range(count):
            bpy.ops.object.duplicate()

        self.report({'INFO'}, f"Duplicated objects {count} times.")
        return {'FINISHED'}


class OBJECT_OT_AlignObjects(bpy.types.Operator):
    bl_idname = "object.align_objects"
    bl_label = "Align Objects"

    def execute(self, context):
        axis = context.scene.align_axis
        for obj in context.selected_objects:
            if axis == 'X':
                obj.location.y = 0
                obj.location.z = 0
            elif axis == 'Y':
                obj.location.x = 0
                obj.location.z = 0
            elif axis == 'Z':
                obj.location.x = 0
                obj.location.y = 0

        self.report({'INFO'}, f"Objects aligned to {axis}-axis.")
        return {'FINISHED'}


class OBJECT_OT_RandomizeObjects(bpy.types.Operator):
    bl_idname = "object.randomize_objects"
    bl_label = "Randomize Objects"

    def execute(self, context):
        for obj in context.selected_objects:
            if context.scene.randomize_position:
                obj.location.x += random.uniform(-1, 1)
                obj.location.y += random.uniform(-1, 1)
                obj.location.z += random.uniform(-1, 1)

            if context.scene.randomize_rotation:
                obj.rotation_euler.x += random.uniform(-1, 1)
                obj.rotation_euler.y += random.uniform(-1, 1)
                obj.rotation_euler.z += random.uniform(-1, 1)

            if context.scene.randomize_scale:
                obj.scale.x *= random.uniform(0.5, 1.5)
                obj.scale.y *= random.uniform(0.5, 1.5)
                obj.scale.z *= random.uniform(0.5, 1.5)

        self.report({'INFO'}, "Objects randomized.")
        return {'FINISHED'}


class OBJECT_OT_ColorizeObjects(bpy.types.Operator):
    bl_idname = "object.colorize_objects"
    bl_label = "Colorize Objects"

    def execute(self, context):
        random_color = context.scene.random_color
        color = context.scene.color
        alpha = context.scene.color_alpha
        scope = context.scene.colorize_scope

        if scope == 'SELECTED':
            objects = context.selected_objects
            if not objects:
                self.report({'WARNING'}, "No objects selected. Select objects to colorize.")
                return {'CANCELLED'}
        elif scope == 'ALL':
            objects = bpy.data.objects

        for obj in objects:
            if obj.type == 'MESH':
                if random_color:
                    color = (random.random(), random.random(), random.random(), 1.0)
                else:
                    color = (*context.scene.color, context.scene.color_alpha)
                
                if obj.data.materials:
                    obj.data.materials[0].diffuse_color = color
                else:
                    mat = bpy.data.materials.new(name="Colorized Material")
                    mat.diffuse_color = color
                    obj.data.materials.append(mat)
        
        self.report({'INFO'}, "Objects colorized.")
        return {'FINISHED'}
    

class OBJECT_OT_MergeObjects(bpy.types.Operator):
    """Merges selected objects into a single object"""
    bl_idname = "object.merge_objects"
    bl_label = "Merge Objects"

    def execute(self, context):
        bpy.ops.object.join()
        self.report({'INFO'}, "Objects merged.")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(OBJECT_PT_CustomPanel)
    bpy.utils.register_class(OBJECT_OT_RenameSelectedObjects)
    bpy.utils.register_class(OBJECT_OT_CleanupScene)
    bpy.utils.register_class(OBJECT_OT_ExportHelper)
    bpy.utils.register_class(OBJECT_OT_OrganizeHierarchy)
    bpy.utils.register_class(OBJECT_OT_RenameCollections)
    bpy.utils.register_class(OBJECT_OT_DuplicateObjects)
    bpy.utils.register_class(OBJECT_OT_AlignObjects)
    bpy.utils.register_class(OBJECT_OT_RandomizeObjects)
    bpy.utils.register_class(OBJECT_OT_ColorizeObjects)
    bpy.utils.register_class(OBJECT_OT_MergeObjects)

    bpy.types.Scene.renamer_prefix = bpy.props.StringProperty(name="Prefix")
    bpy.types.Scene.renamer_suffix = bpy.props.StringProperty(name="Suffix")
    bpy.types.Scene.renamer_numbering = bpy.props.BoolProperty(name="Numbering", default=False)
    bpy.types.Scene.renamer_start_number = bpy.props.IntProperty(name="Start Number", default=1)
    bpy.types.Scene.cleanup_unused_materials = bpy.props.BoolProperty(name="Unused Materials", default=True)
    bpy.types.Scene.cleanup_unused_textures = bpy.props.BoolProperty(name="Unused Textures", default=True)
    bpy.types.Scene.cleanup_unused_meshes = bpy.props.BoolProperty(name="Unused Meshes", default=True)
    bpy.types.Scene.export_format = bpy.props.EnumProperty(
        name="Format",
        items=[('FBX', "FBX", ""), ('GLTF', "glTF", ""), ('OBJ', "OBJ", "")]
    )
    bpy.types.Scene.export_scope = bpy.props.EnumProperty(
        name="Scope",
        items=[('ALL', "All Objects", ""), ('SELECTED', "Selected Only", "")]
    )
    bpy.types.Scene.export_apply_modifiers = bpy.props.BoolProperty(name="Apply Modifiers", default=False)
    bpy.types.Scene.export_include_animation = bpy.props.BoolProperty(name="Include Animation", default=False)
    bpy.types.Scene.export_embed_textures = bpy.props.BoolProperty(name="Embed Textures", default=False)
    bpy.types.Scene.export_compress = bpy.props.BoolProperty(name="Compress", default=False)
    bpy.types.Scene.collection_renamer_prefix = bpy.props.StringProperty(name="Prefix")
    bpy.types.Scene.collection_renamer_suffix = bpy.props.StringProperty(name="Suffix")
    bpy.types.Scene.duplicate_count = bpy.props.IntProperty(name="Duplicate Count", default=1, min=1)
    bpy.types.Scene.align_axis = bpy.props.EnumProperty(
        name="Axis",
        items=[('X', "X", ""), ('Y', "Y", ""), ('Z', "Z", "")]
    )
    bpy.types.Scene.randomize_position = bpy.props.BoolProperty(name="Randomize Position", default=True)
    bpy.types.Scene.randomize_rotation = bpy.props.BoolProperty(name="Randomize Rotation", default=False)
    bpy.types.Scene.randomize_scale = bpy.props.BoolProperty(name="Randomize Scale", default=False)
    bpy.types.Scene.random_color = bpy.props.BoolProperty(name="Random Color", default=True)

    bpy.types.Scene.color = bpy.props.FloatVectorProperty(
        name="Color",
        default=(1.0, 1.0, 1.0),
        subtype='COLOR',
        min=0.0,
        max=1.0
    )
    bpy.types.Scene.color_alpha = bpy.props.FloatProperty(
        name="Alpha",
        default=1.0,
        min=0.0,
        max=1.0
    )

    bpy.types.Scene.colorize_scope = bpy.props.EnumProperty(
        name="Scope",
        items=[('SELECTED', "Selected Objects", ""), ('ALL', "All Objects", "")]
    )

    bpy.types.Scene.expand_renamer = bpy.props.BoolProperty(name="Expand Renamer", default=True)
    bpy.types.Scene.expand_cleanup = bpy.props.BoolProperty(name="Expand Cleanup", default=True)
    bpy.types.Scene.expand_export = bpy.props.BoolProperty(name="Expand Export", default=True)
    bpy.types.Scene.expand_hierarchy = bpy.props.BoolProperty(name="Expand Hierarchy", default=True)
    bpy.types.Scene.expand_duplicator = bpy.props.BoolProperty(name="Expand Duplicator", default=True)
    bpy.types.Scene.expand_aligner = bpy.props.BoolProperty(name="Expand Aligner", default=True)
    bpy.types.Scene.expand_randomizer = bpy.props.BoolProperty(name="Expand Randomizer", default=True)
    bpy.types.Scene.expand_colorizer = bpy.props.BoolProperty(name="Expand Colorizer", default=True)
    bpy.types.Scene.expand_merger = bpy.props.BoolProperty(name="Expand Merger", default=True)

def unregister():
    bpy.utils.unregister_class(OBJECT_PT_CustomPanel)
    bpy.utils.unregister_class(OBJECT_OT_RenameSelectedObjects)
    bpy.utils.unregister_class(OBJECT_OT_CleanupScene)
    bpy.utils.unregister_class(OBJECT_OT_ExportHelper)
    bpy.utils.unregister_class(OBJECT_OT_OrganizeHierarchy)
    bpy.utils.unregister_class(OBJECT_OT_RenameCollections)
    bpy.utils.unregister_class(OBJECT_OT_DuplicateObjects)
    bpy.utils.unregister_class(OBJECT_OT_AlignObjects)
    bpy.utils.unregister_class(OBJECT_OT_RandomizeObjects)
    bpy.utils.unregister_class(OBJECT_OT_ColorizeObjects)
    bpy.utils.unregister_class(OBJECT_OT_MergeObjects)

    del bpy.types.Scene.renamer_prefix
    del bpy.types.Scene.renamer_suffix
    del bpy.types.Scene.renamer_numbering
    del bpy.types.Scene.renamer_start_number
    del bpy.types.Scene.cleanup_unused_materials
    del bpy.types.Scene.cleanup_unused_textures
    del bpy.types.Scene.cleanup_unused_meshes
    del bpy.types.Scene.export_format
    del bpy.types.Scene.export_scope
    del bpy.types.Scene.export_apply_modifiers
    del bpy.types.Scene.export_include_animation
    del bpy.types.Scene.export_embed_textures
    del bpy.types.Scene.export_compress
    del bpy.types.Scene.collection_renamer_prefix
    del bpy.types.Scene.collection_renamer_suffix
    del bpy.types.Scene.duplicate_count
    del bpy.types.Scene.align_axis
    del bpy.types.Scene.randomize_position
    del bpy.types.Scene.randomize_rotation
    del bpy.types.Scene.randomize_scale
    del bpy.types.Scene.random_color
    del bpy.types.Scene.color 
    del bpy.types.Scene.color_alpha 
    del bpy.types.Scene.colorize_scope 

    del bpy.types.Scene.expand_renamer
    del bpy.types.Scene.expand_cleanup
    del bpy.types.Scene.expand_export
    del bpy.types.Scene.expand_hierarchy
    del bpy.types.Scene.expand_duplicator
    del bpy.types.Scene.expand_aligner
    del bpy.types.Scene.expand_randomizer
    del bpy.types.Scene.expand_colorizer
    del bpy.types.Scene.expand_merger

if __name__ == "__main__":
    register()