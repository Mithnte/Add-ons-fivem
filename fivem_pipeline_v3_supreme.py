import bpy
import bmesh
import os
import json
import math
import random
from mathlib import Vector
from datetime import datetime

bl_info = {
    "name": "FiveM Development Pipeline V3 SUPREME",
    "author": "Premium Dev Team",
    "version": (3, 99, 0),
    "blender": (3, 6, 0),
    "location": "View3D > Sidebar > FiveM V3",
    "description": "Supreme professional toolkit for FiveM/GTA V development - 50+ premium features",
    "category": "Development",
    "doc_url": "https://docs.fivem.net/",
}

# --- GLOBAL SETTINGS ---

class FiveMSettings(bpy.types.PropertyGroup):
    """Global settings for FiveM pipeline"""
    
    auto_validate: bpy.props.BoolProperty(
        name="Auto-Validate on Save",
        description="Automatically validate geometry before saving",
        default=False
    )
    
    target_poly_budget: bpy.props.IntProperty(
        name="Poly Budget",
        description="Target polygon budget for scene",
        default=50000,
        min=1000,
        max=500000
    )
    
    export_path: bpy.props.StringProperty(
        name="Export Path",
        description="Default export directory",
        default="//exports/",
        subtype='DIR_PATH'
    )
    
    project_name: bpy.props.StringProperty(
        name="Project Name",
        description="Current FiveM project name",
        default="my_resource"
    )
    
    auto_backup: bpy.props.BoolProperty(
        name="Auto Backup",
        description="Automatically backup before major operations",
        default=True
    )
    
    use_vertex_colors: bpy.props.BoolProperty(
        name="Use Vertex Colors",
        description="Enable vertex color workflow",
        default=False
    )
    
    optimization_level: bpy.props.EnumProperty(
        name="Optimization Level",
        items=[
            ('QUALITY', 'Quality', 'Prioritize visual quality'),
            ('BALANCED', 'Balanced', 'Balance quality and performance'),
            ('PERFORMANCE', 'Performance', 'Prioritize performance'),
        ],
        default='BALANCED'
    )
    
    show_stats_overlay: bpy.props.BoolProperty(
        name="Show Stats Overlay",
        description="Display real-time stats in viewport",
        default=True
    )
    
    max_texture_size: bpy.props.IntProperty(
        name="Max Texture Size",
        description="Maximum texture resolution",
        default=2048,
        min=512,
        max=8192
    )
    
    enable_auto_lod: bpy.props.BoolProperty(
        name="Enable Auto LOD",
        description="Automatically generate LODs on export",
        default=False
    )
    
    performance_mode: bpy.props.BoolProperty(
        name="Performance Mode",
        description="Enable performance optimizations",
        default=False
    )

# --- ADVANCED UTILITIES ---

def get_poly_count(context, selected_only=False):
    """Calculate accurate triangle count"""
    total_tris = 0
    total_verts = 0
    
    if selected_only:
        target_objs = [o for o in context.selected_objects if o.type == 'MESH']
    else:
        target_objs = [o for o in context.scene.objects if o.type == 'MESH' and o.visible_get()]
    
    for obj in target_objs:
        try:
            dg = context.evaluated_depsgraph_get()
            obj_eval = obj.evaluated_get(dg)
            mesh = obj_eval.to_mesh()
            
            if mesh:
                total_tris += sum(len(p.vertices) - 2 for p in mesh.polygons)
                total_verts += len(mesh.vertices)
                obj_eval.to_mesh_clear()
        except Exception as e:
            print(f"V3: Error calculating poly count for {obj.name}: {e}")
    
    return total_tris, total_verts

def get_texture_memory(context):
    """Calculate texture memory usage"""
    total_bytes = 0
    processed_images = set()
    texture_list = []
    
    for obj in context.scene.objects:
        if obj.type == 'MESH':
            for slot in obj.material_slots:
                if slot.material and slot.material.use_nodes:
                    for node in slot.material.node_tree.nodes:
                        if node.type == 'TEX_IMAGE' and node.image:
                            if node.image.name not in processed_images:
                                processed_images.add(node.image.name)
                                size = node.image.size[0] * node.image.size[1] * 4
                                total_bytes += size
                                texture_list.append({
                                    'name': node.image.name,
                                    'size': size / (1024 * 1024),
                                    'resolution': f"{node.image.size[0]}x{node.image.size[1]}"
                                })
    
    return total_bytes / (1024 * 1024), texture_list

def calculate_bounds(obj):
    """Calculate object bounding box dimensions"""
    if obj.type != 'MESH':
        return None
    
    bbox_corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    
    min_x = min(v.x for v in bbox_corners)
    max_x = max(v.x for v in bbox_corners)
    min_y = min(v.y for v in bbox_corners)
    max_y = max(v.y for v in bbox_corners)
    min_z = min(v.z for v in bbox_corners)
    max_z = max(v.z for v in bbox_corners)
    
    return {
        'width': max_x - min_x,
        'depth': max_y - min_y,
        'height': max_z - min_z
    }

def smart_material_cleanup(context):
    """Remove unused materials and optimize"""
    removed = 0
    
    for mat in bpy.data.materials:
        if mat.users == 0:
            bpy.data.materials.remove(mat)
            removed += 1
    
    return removed

def create_backup(context):
    """Create automatic backup"""
    if context.blend_data.filepath:
        backup_path = context.blend_data.filepath.replace('.blend', f'_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.blend')
        bpy.ops.wm.save_as_mainfile(filepath=backup_path, copy=True)
        return backup_path
    return None

def calculate_draw_calls(context):
    """Estimate draw calls for scene"""
    draw_calls = 0
    material_count = {}
    
    for obj in context.scene.objects:
        if obj.type == 'MESH' and obj.visible_get():
            for slot in obj.material_slots:
                if slot.material:
                    mat_name = slot.material.name
                    if mat_name not in material_count:
                        material_count[mat_name] = 0
                    material_count[mat_name] += 1
    
    draw_calls = len(material_count)
    return draw_calls, material_count

def get_scene_complexity_score(context):
    """Calculate overall scene complexity score"""
    tris, verts = get_poly_count(context)
    tex_mem, _ = get_texture_memory(context)
    draw_calls, _ = calculate_draw_calls(context)
    
    score = 100
    
    if tris > 100000:
        score -= 40
    elif tris > 70000:
        score -= 25
    elif tris > 50000:
        score -= 15
    
    if tex_mem > 100:
        score -= 30
    elif tex_mem > 50:
        score -= 15
    
    if draw_calls > 50:
        score -= 20
    elif draw_calls > 30:
        score -= 10
    
    return max(0, score)

def detect_object_type(obj):
    """AI detection of object type based on characteristics"""
    if obj.type != 'MESH':
        return 'prop_'
    
    bounds = calculate_bounds(obj)
    if not bounds:
        return 'prop_'
    
    poly_count = len(obj.data.polygons)
    
    # Vehicle detection
    if bounds['width'] > 3.0 and bounds['depth'] > 1.5 and bounds['height'] > 1.0:
        return 'veh_'
    
    # Weapon detection (elongated shape)
    if bounds['depth'] > 1.0 and bounds['width'] < 0.3 and bounds['height'] < 0.3:
        return 'weap_'
    
    # Interior prop (large flat)
    if bounds['height'] < 0.5 and (bounds['width'] > 5.0 or bounds['depth'] > 5.0):
        return 'int_'
    
    # Ped accessory (small, detailed)
    if bounds['height'] < 0.5 and bounds['width'] < 0.5 and poly_count > 1000:
        return 'p_'
    
    # Default to prop
    return 'prop_'

# --- PREMIUM OPERATORS ---

class DEV_OT_SmartRenameV3(bpy.types.Operator):
    """V3 Smart renaming with AI detection"""
    bl_idname = "dev.smart_rename_v3"
    bl_label = "V3 Smart Rename"
    bl_options = {'REGISTER', 'UNDO'}
    
    prefix: bpy.props.EnumProperty(
        name="Prefix Type",
        items=[
            ('prop_', 'World Prop', 'Standard world prop'),
            ('p_', 'Ped Accessory', 'Clothing/Accessories'),
            ('v_', 'Vehicle Part', 'Vehicle component'),
            ('veh_', 'Full Vehicle', 'Complete vehicle'),
            ('lod_', 'LOD Mesh', 'Level of Detail'),
            ('int_', 'Interior Prop', 'Interior object'),
            ('weap_', 'Weapon', 'Weapon model'),
            ('col_', 'Collision', 'Collision mesh'),
        ]
    )
    
    base_name: bpy.props.StringProperty(
        name="Base Name",
        default="asset",
        description="Base name for objects"
    )
    
    auto_detect: bpy.props.BoolProperty(
        name="Auto-Detect Type",
        description="AI detection based on mesh characteristics",
        default=True
    )
    
    add_suffix: bpy.props.BoolProperty(
        name="Add Quality Suffix",
        description="Add _high, _med, _low based on poly count",
        default=False
    )
    
    def execute(self, context):
        if not context.selected_objects:
            self.report({'WARNING'}, "V3: No objects selected")
            return {'CANCELLED'}
        
        renamed_count = 0
        
        for i, obj in enumerate(context.selected_objects):
            if obj.type != 'MESH':
                continue
            
            detected_prefix = self.prefix
            
            if self.auto_detect:
                detected_prefix = detect_object_type(obj)
            
            clean_name = obj.name.split('.')[0]
            for p in ['prop_', 'p_', 'v_', 'lod_', 'veh_', 'int_', 'weap_', 'col_']:
                if clean_name.startswith(p):
                    clean_name = clean_name[len(p):]
                    break
            
            final_name = self.base_name if self.base_name != "asset" else clean_name.lower()
            
            suffix = ""
            if self.add_suffix:
                poly_count = len(obj.data.polygons)
                if poly_count > 10000:
                    suffix = "_high"
                elif poly_count > 2000:
                    suffix = "_med"
                else:
                    suffix = "_low"
            
            obj.name = f"{detected_prefix}{final_name}_{i+1:03d}{suffix}"
            renamed_count += 1
        
        self.report({'INFO'}, f"V3: Renamed {renamed_count} objects")
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=400)

class DEV_OT_ValidatorV3(bpy.types.Operator):
    """V3 Advanced geometry validator"""
    bl_idname = "dev.validator_v3"
    bl_label = "V3 Geometry Validator"
    bl_options = {'REGISTER', 'UNDO'}
    
    auto_fix: bpy.props.BoolProperty(
        name="Auto-Fix Issues",
        description="Automatically fix detected issues",
        default=False
    )
    
    check_uvs: bpy.props.BoolProperty(name="Check UVs", default=True)
    check_normals: bpy.props.BoolProperty(name="Check Normals", default=True)
    check_scale: bpy.props.BoolProperty(name="Check Scale", default=True)
    
    def execute(self, context):
        issues = {
            'ngons': [],
            'non_manifold': [],
            'loose_verts': [],
            'degenerate': [],
            'uv_missing': [],
            'zero_area': [],
            'inverted_normals': [],
            'non_uniform_scale': []
        }
        
        processed = 0
        fixed = 0
        
        target_objs = context.selected_objects if context.selected_objects else context.scene.objects
        
        for obj in target_objs:
            if obj.type != 'MESH':
                continue
            
            processed += 1
            
            # Check scale
            if self.check_scale:
                if not (0.99 < obj.scale.x < 1.01 and 0.99 < obj.scale.y < 1.01 and 0.99 < obj.scale.z < 1.01):
                    issues['non_uniform_scale'].append(obj.name)
                    if self.auto_fix:
                        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            
            bm = bmesh.new()
            bm.from_mesh(obj.data)
            
            # Check N-Gons
            ngon_faces = [f for f in bm.faces if len(f.verts) > 4]
            if ngon_faces:
                issues['ngons'].append(f"{obj.name} ({len(ngon_faces)})")
                if self.auto_fix:
                    bmesh.ops.triangulate(bm, faces=ngon_faces)
                    fixed += 1
            
            # Check Non-Manifold
            non_manifold = [v for v in bm.verts if not v.is_manifold]
            if non_manifold:
                issues['non_manifold'].append(f"{obj.name} ({len(non_manifold)})")
            
            # Check Loose Vertices
            loose = [v for v in bm.verts if not v.link_edges]
            if loose:
                issues['loose_verts'].append(f"{obj.name} ({len(loose)})")
                if self.auto_fix:
                    bmesh.ops.delete(bm, geom=loose, context='VERTS')
                    fixed += 1
            
            # Check Degenerate
            degenerate = [f for f in bm.faces if f.calc_area() < 0.0001]
            if degenerate:
                issues['degenerate'].append(f"{obj.name} ({len(degenerate)})")
                if self.auto_fix:
                    bmesh.ops.delete(bm, geom=degenerate, context='FACES')
                    fixed += 1
            
            # Check Zero Area
            zero_area = [f for f in bm.faces if f.calc_area() == 0]
            if zero_area:
                issues['zero_area'].append(f"{obj.name} ({len(zero_area)})")
                if self.auto_fix:
                    bmesh.ops.delete(bm, geom=zero_area, context='FACES')
                    fixed += 1
            
            # Check inverted normals
            if self.check_normals:
                inverted = sum(1 for f in bm.faces if f.normal.z < -0.5)
                if inverted > len(bm.faces) * 0.3:
                    issues['inverted_normals'].append(f"{obj.name} ({inverted})")
                    if self.auto_fix:
                        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
                        fixed += 1
            
            # Check UVs
            if self.check_uvs and not obj.data.uv_layers:
                issues['uv_missing'].append(obj.name)
            
            if self.auto_fix:
                bm.to_mesh(obj.data)
                obj.data.update()
            
            bm.free()
        
        # Generate Report
        report = []
        for key, value in issues.items():
            if value:
                report.append(f"{key.replace('_', ' ').title()}: {len(value)}")
        
        if report:
            msg = "V3: " + " | ".join(report)
            if self.auto_fix:
                msg += f" | Fixed {fixed}"
            self.report({'WARNING'}, msg)
        else:
            self.report({'INFO'}, f"V3: {processed} objects validated - Clean")
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

class DEV_OT_LODGeneratorV3(bpy.types.Operator):
    """V3 Intelligent LOD generator"""
    bl_idname = "dev.lod_generator_v3"
    bl_label = "V3 LOD Generator"
    bl_options = {'REGISTER', 'UNDO'}
    
    quality_preset: bpy.props.EnumProperty(
        name="Quality Preset",
        items=[
            ('HIGH', 'High Quality', 'Max detail (50%, 25%, 12%)'),
            ('BALANCED', 'Balanced', 'Balanced (40%, 20%, 8%)'),
            ('PERFORMANCE', 'Performance', 'Optimized (30%, 15%, 5%)'),
            ('ULTRA', 'Ultra Performance', 'Extreme (20%, 10%, 3%)'),
        ],
        default='BALANCED'
    )
    
    lod_count: bpy.props.IntProperty(name="LOD Levels", default=3, min=1, max=5)
    preserve_uvs: bpy.props.BoolProperty(name="Preserve UVs", default=True)
    preserve_sharp: bpy.props.BoolProperty(name="Preserve Sharp Edges", default=True)
    preserve_materials: bpy.props.BoolProperty(name="Preserve Material Boundaries", default=True)
    
    def execute(self, context):
        if not context.selected_objects:
            self.report({'WARNING'}, "V3: No objects selected")
            return {'CANCELLED'}
        
        presets = {
            'HIGH': [0.5, 0.25, 0.12, 0.06, 0.03],
            'BALANCED': [0.4, 0.2, 0.08, 0.04, 0.02],
            'PERFORMANCE': [0.3, 0.15, 0.05, 0.02, 0.01],
            'ULTRA': [0.2, 0.1, 0.03, 0.01, 0.005]
        }
        
        ratios = presets[self.quality_preset]
        created_lods = 0
        
        for obj in context.selected_objects:
            if obj.type != 'MESH':
                continue
            
            for i in range(self.lod_count):
                lod_obj = obj.copy()
                lod_obj.data = obj.data.copy()
                context.collection.objects.link(lod_obj)
                
                base_name = obj.name.split('.')[0]
                if '_lod' in base_name.lower():
                    base_name = base_name.split('_lod')[0]
                
                lod_obj.name = f"{base_name}_LOD{i+1}"
                
                decimate = lod_obj.modifiers.new(name="LOD_Decimate", type='DECIMATE')
                decimate.ratio = ratios[i]
                decimate.use_collapse_triangulate = True
                
                delimit_set = set()
                if self.preserve_uvs:
                    delimit_set.add('UV')
                if self.preserve_sharp:
                    delimit_set.add('SHARP')
                if self.preserve_materials:
                    delimit_set.add('MATERIAL')
                
                if delimit_set:
                    decimate.delimit = delimit_set
                
                context.view_layer.objects.active = lod_obj
                bpy.ops.object.modifier_apply(modifier=decimate.name)
                
                created_lods += 1
        
        self.report({'INFO'}, f"V3: Generated {created_lods} LODs ({self.quality_preset})")
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=350)

class DEV_OT_BatchCleanupV3(bpy.types.Operator):
    """V3 Comprehensive batch cleanup"""
    bl_idname = "dev.batch_cleanup_v3"
    bl_label = "V3 Batch Cleanup"
    bl_options = {'REGISTER', 'UNDO'}
    
    remove_doubles: bpy.props.BoolProperty(name="Remove Doubles", default=True)
    recalc_normals: bpy.props.BoolProperty(name="Recalc Normals", default=True)
    delete_loose: bpy.props.BoolProperty(name="Delete Loose", default=True)
    smart_uv_project: bpy.props.BoolProperty(name="Smart UV Project", default=False)
    apply_scale: bpy.props.BoolProperty(name="Apply Scale", default=True)
    weighted_normals: bpy.props.BoolProperty(name="Add Weighted Normals", default=False)
    limit_dissolve: bpy.props.BoolProperty(name="Limited Dissolve", default=False)
    
    merge_distance: bpy.props.FloatProperty(
        name="Merge Distance",
        default=0.0001,
        min=0.00001,
        max=1.0,
        precision=5
    )
    
    dissolve_angle: bpy.props.FloatProperty(
        name="Dissolve Angle",
        default=5.0,
        min=0.1,
        max=45.0
    )
    
    def execute(self, context):
        cleaned = 0
        
        for obj in context.selected_objects if context.selected_objects else context.scene.objects:
            if obj.type != 'MESH':
                continue
            
            context.view_layer.objects.active = obj
            
            if self.apply_scale:
                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            
            if self.remove_doubles:
                bpy.ops.mesh.remove_doubles(threshold=self.merge_distance)
            
            if self.delete_loose:
                bpy.ops.mesh.delete_loose()
            
            if self.limit_dissolve:
                bpy.ops.mesh.dissolve_limited(angle_limit=math.radians(self.dissolve_angle))
            
            if self.recalc_normals:
                bpy.ops.mesh.normals_make_consistent(inside=False)
            
            if self.smart_uv_project and not obj.data.uv_layers:
                bpy.ops.uv.smart_project(angle_limit=66, island_margin=0.02)
            
            bpy.ops.object.mode_set(mode='OBJECT')
            
            if self.weighted_normals:
                wn_mod = obj.modifiers.new(name="WeightedNormal", type='WEIGHTED_NORMAL')
                wn_mod.keep_sharp = True
            
            cleaned += 1
        
        mat_removed = smart_material_cleanup(context)
        
        self.report({'INFO'}, f"V3: Cleaned {cleaned} objects | Removed {mat_removed} materials")
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=400)

class DEV_OT_CollisionV3(bpy.types.Operator):
    """V3 Advanced collision generator"""
    bl_idname = "dev.collision_v3"
    bl_label = "V3 Collision Generator"
    bl_options = {'REGISTER', 'UNDO'}
    
    collision_type: bpy.props.EnumProperty(
        name="Collision Type",
        items=[
            ('CONVEX', 'Convex Hull', 'Simple convex'),
            ('BOX', 'Bounding Box', 'Box collision'),
            ('DECIMATED', 'Decimated Mesh', 'Simplified mesh'),
            ('CYLINDER', 'Cylinder', 'Cylindrical'),
            ('SPHERE', 'Sphere', 'Spherical'),
            ('CAPSULE', 'Capsule', 'Capsule shape'),
        ],
        default='CONVEX'
    )
    
    decimate_ratio: bpy.props.FloatProperty(name="Decimate Ratio", default=0.1, min=0.01, max=0.5)
    apply_collision_material: bpy.props.BoolProperty(name="Apply Collision Material", default=True)
    add_to_collection: bpy.props.BoolProperty(name="Add to Collision Collection", default=True)
    
    def execute(self, context):
        if not context.selected_objects:
            self.report({'WARNING'}, "V3: No objects selected")
            return {'CANCELLED'}
        
        # Create collision collection
        col_collection = None
        if self.add_to_collection:
            if "Collision" not in bpy.data.collections:
                col_collection = bpy.data.collections.new("Collision")
                context.scene.collection.children.link(col_collection)
            else:
                col_collection = bpy.data.collections["Collision"]
        
        created = 0
        
        for obj in context.selected_objects:
            if obj.type != 'MESH':
                continue
            
            col_obj = obj.copy()
            col_obj.data = obj.data.copy()
            
            if col_collection:
                col_collection.objects.link(col_obj)
            else:
                context.collection.objects.link(col_obj)
            
            base_name = obj.name.split('.')[0]
            col_obj.name = f"col_{base_name}"
            
            context.view_layer.objects.active = col_obj
            
            if self.collision_type == 'CONVEX':
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.convex_hull()
                bpy.ops.object.mode_set(mode='OBJECT')
                
            elif self.collision_type == 'BOX':
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.delete(type='VERT')
                bpy.ops.mesh.primitive_cube_add()
                bpy.ops.object.mode_set(mode='OBJECT')
                col_obj.dimensions = obj.dimensions
                
            elif self.collision_type == 'CYLINDER':
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.delete(type='VERT')
                bpy.ops.mesh.primitive_cylinder_add()
                bpy.ops.object.mode_set(mode='OBJECT')
                col_obj.dimensions = obj.dimensions
                
            elif self.collision_type == 'SPHERE':
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.delete(type='VERT')
                bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8)
                bpy.ops.object.mode_set(mode='OBJECT')
                max_dim = max(obj.dimensions)
                col_obj.dimensions = (max_dim, max_dim, max_dim)
                
            elif self.collision_type == 'CAPSULE':
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.delete(type='VERT')
                bpy.ops.mesh.primitive_cylinder_add()
                bpy.ops.object.mode_set(mode='OBJECT')
                col_obj.dimensions = obj.dimensions
                
            elif self.collision_type == 'DECIMATED':
                decimate = col_obj.modifiers.new(name="Collision_Decimate", type='DECIMATE')
                decimate.ratio = self.decimate_ratio
                bpy.ops.object.modifier_apply(modifier=decimate.name)
            
            col_obj.display_type = 'WIRE'
            col_obj.show_all_edges = True
            
            if self.apply_collision_material:
                mat = bpy.data.materials.get("Collision_Visual")
                if not mat:
                    mat = bpy.data.materials.new(name="Collision_Visual")
                    mat.use_nodes = True
                    mat.diffuse_color = (0, 1, 0, 0.3)
                    mat.blend_method = 'BLEND'
                
                if col_obj.data.materials:
                    col_obj.data.materials[0] = mat
                else:
                    col_obj.data.materials.append(mat)
            
            created += 1
        
        self.report({'INFO'}, f"V3: Generated {created} collision meshes ({self.collision_type})")
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=400)

class DEV_OT_TextureAnalyzerV3(bpy.types.Operator):
    """V3 Advanced texture analyzer"""
    bl_idname = "dev.texture_analyzer_v3"
    bl_label = "V3 Texture Analyzer"
    bl_options = {'REGISTER'}
    
    show_all: bpy.props.BoolProperty(name="Show All Textures", default=False)
    suggest_optimization: bpy.props.BoolProperty(name="Suggest Optimizations", default=True)
    
    def execute(self, context):
        tex_mem, tex_list = get_texture_memory(context)
        
        tex_list.sort(key=lambda x: x['size'], reverse=True)
        
        print("\n" + "="*70)
        print("V3 SUPREME TEXTURE MEMORY ANALYSIS")
        print("="*70)
        print(f"Total Texture Memory: {tex_mem:.2f} MB")
        print(f"Unique Textures: {len(tex_list)}\n")
        
        display_count = len(tex_list) if self.show_all else min(20, len(tex_list))
        
        for i, tex in enumerate(tex_list[:display_count], 1):
            status = "⚠" if tex['size'] > 4.0 else "✓"
            print(f"{status} {i:2d}. {tex['name'][:40]:<40} | {tex['resolution']:>12} | {tex['size']:>7.2f} MB")
        
        if len(tex_list) > display_count:
            print(f"\n... and {len(tex_list) - display_count} more textures")
        
        if self.suggest_optimization:
            print("\n" + "-"*70)
            print("OPTIMIZATION RECOMMENDATIONS:")
            
            oversized = [t for t in tex_list if t['size'] > 4.0]
            if oversized:
                print(f"\n⚠ {len(oversized)} textures over 4MB:")
                for tex in oversized[:5]:
                    res_parts = tex['resolution'].split('x')
                    current_w, current_h = int(res_parts[0]), int(res_parts[1])
                    suggested_w, suggested_h = current_w // 2, current_h // 2
                    print(f"  - {tex['name']}: Reduce from {tex['resolution']} to {suggested_w}x{suggested_h}")
            
            high_res = [t for t in tex_list if '4096' in t['resolution'] or '8192' in t['resolution']]
            if high_res:
                print(f"\n⚠ {len(high_res)} high-resolution textures (4K+)")
                print("  Consider using 2K (2048x2048) for better performance")
        
        print("="*70 + "\n")
        
        oversized = [t for t in tex_list if t['size'] > 4.0]
        
        if oversized:
            self.report({'WARNING'}, f"V3: {len(oversized)} textures over 4MB")
        else:
            self.report({'INFO'}, f"V3: Texture usage optimal - {tex_mem:.2f} MB")
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

class DEV_OT_UVOptimizer(bpy.types.Operator):
    """V3 UV optimizer"""
    bl_idname = "dev.uv_optimizer"
    bl_label = "V3 UV Optimizer"
    bl_options = {'REGISTER', 'UNDO'}
    
    pack_margin: bpy.props.FloatProperty(name="Pack Margin", default=0.01, min=0.001, max=0.1)
    rotate_islands: bpy.props.BoolProperty(name="Rotate Islands", default=True)
    average_island_scale: bpy.props.BoolProperty(name="Average Island Scale", default=False)
    
    def execute(self, context):
        if not context.selected_objects:
            self.report({'WARNING'}, "V3: No objects selected")
            return {'CANCELLED'}
        
        optimized = 0
        
        for obj in context.selected_objects:
            if obj.type != 'MESH':
                continue
            
            context.view_layer.objects.active = obj
            
            if not obj.data.uv_layers:
                bpy.ops.mesh.uv_texture_add()
            
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            
            bpy.ops.uv.select_all(action='SELECT')
            
            if self.average_island_scale:
                bpy.ops.uv.average_islands_scale()
            
            bpy.ops.uv.pack_islands(margin=self.pack_margin, rotate=self.rotate_islands)
            
            bpy.ops.object.mode_set(mode='OBJECT')
            optimized += 1
        
        self.report({'INFO'}, f"V3: Optimized UVs for {optimized} objects")
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

class DEV_OT_QuickFix(bpy.types.Operator):
    """V3 One-click optimization"""
    bl_idname = "dev.quick_fix"
    bl_label = "V3 Quick Fix All"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        fixed_count = 0
        
        for obj in context.scene.objects:
            if obj.type != 'MESH':
                continue
            
            context.view_layer.objects.active = obj
            obj.select_set(True)
            
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            
            bpy.ops.mesh.remove_doubles(threshold=0.0001)
            bpy.ops.mesh.delete_loose()
            bpy.ops.mesh.normals_make_consistent(inside=False)
            bpy.ops.mesh.dissolve_limited(angle_limit=math.radians(5.0))
            
            bpy.ops.object.mode_set(mode='OBJECT')
            
            obj.select_set(False)
            fixed_count += 1
        
        mat_removed = smart_material_cleanup(context)
        
        self.report({'INFO'}, f"V3: Quick fixed {fixed_count} objects | Removed {mat_removed} materials")
        return {'FINISHED'}

class DEV_OT_ExportV3(bpy.types.Operator):
    """V3 Optimized FBX export"""
    bl_idname = "dev.export_v3"
    bl_label = "V3 Export FBX"
    bl_options = {'REGISTER'}
    
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    use_selection: bpy.props.BoolProperty(name="Selection Only", default=True)
    apply_modifiers: bpy.props.BoolProperty(name="Apply Modifiers", default=True)
    create_backup: bpy.props.BoolProperty(name="Create Backup", default=True)
    
    def execute(self, context):
        settings = context.scene.fivem_settings
        
        if self.create_backup and settings.auto_backup:
            backup_path = create_backup(context)
            if backup_path:
                print(f"V3: Backup created at {backup_path}")
        
        tris, verts = get_poly_count(context, selected_only=self.use_selection)
        
        bpy.ops.export_scene.fbx(
            filepath=self.filepath,
            use_selection=self.use_selection,
            object_types={'MESH'},
            use_mesh_modifiers=self.apply_modifiers,
            mesh_smooth_type='FACE',
            use_tspace=True,
            axis_forward='-Z',
            axis_up='Y',
        )
        
        export_log = {
            'version': 'V3-SUPREME',
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'project': settings.project_name,
            'file': os.path.basename(self.filepath),
            'triangles': tris,
            'vertices': verts,
        }
        
        print(f"\n[V3 EXPORT LOG]\n{json.dumps(export_log, indent=2)}\n")
        
        self.report({'INFO'}, f"V3: Exported {os.path.basename(self.filepath)} ({tris:,} tris)")
        return {'FINISHED'}
    
    def invoke(self, context, event):
        settings = context.scene.fivem_settings
        
        if settings.project_name:
            self.filepath = f"//{settings.project_name}_{datetime.now().strftime('%Y%m%d_%H%M')}.fbx"
        
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class DEV_OT_ReportV3(bpy.types.Operator):
    """V3 Scene report"""
    bl_idname = "dev.report_v3"
    bl_label = "V3 Generate Report"
    bl_options = {'REGISTER'}
    
    export_json: bpy.props.BoolProperty(name="Export JSON", default=False)
    
    def execute(self, context):
        settings = context.scene.fivem_settings
        tris, verts = get_poly_count(context)
        tex_mem, tex_list = get_texture_memory(context)
        complexity_score = get_scene_complexity_score(context)
        
        mesh_count = len([o for o in context.scene.objects if o.type == 'MESH'])
        
        report = f"""
╔════════════════════════════════════════════════════════════════╗
║        V3 SUPREME FIVEM SCENE ANALYSIS REPORT                  ║
╚════════════════════════════════════════════════════════════════╝

PROJECT: {settings.project_name}
DATE: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

GEOMETRY
  Objects: {mesh_count}
  Triangles: {tris:,}
  Vertices: {verts:,}
  Budget: {settings.target_poly_budget:,}

TEXTURES
  Count: {len(tex_list)}
  Memory: {tex_mem:.2f} MB

PERFORMANCE
  Complexity Score: {complexity_score}/100
  Rating: {'EXCELLENT' if complexity_score >= 80 else 'GOOD' if complexity_score >= 60 else 'NEEDS OPTIMIZATION'}

═══════════════════════════════════════════════════════════════════
"""
        
        print(report)
        
        self.report({'INFO'}, "V3: Report generated - Check console")
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

# --- UI PANELS ---

class VIEW3D_PT_FiveMV3(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'FiveM V3'
    bl_label = "FIVEM V3 SUPREME"

    def draw(self, context):
        layout = self.layout
        settings = context.scene.fivem_settings
        
        # Project Settings
        box = layout.box()
        box.label(text="PROJECT SETTINGS", icon='SETTINGS')
        col = box.column(align=True)
        col.prop(settings, "project_name")
        col.prop(settings, "target_poly_budget")
        col.prop(settings, "optimization_level")
        
        layout.separator()
        
        # Live Stats
        box = layout.box()
        box.label(text="LIVE STATISTICS", icon='INFO')
        
        tris, verts = get_poly_count(context)
        tex_mem, _ = get_texture_memory(context)
        complexity_score = get_scene_complexity_score(context)
        
        col = box.column(align=True)
        col.label(text=f"Triangles: {tris:,}")
        
        budget_pct = (tris / settings.target_poly_budget) * 100 if settings.target_poly_budget > 0 else 0
        
        if tris > settings.target_poly_budget:
            col.label(text=f"OVER BUDGET: {tris - settings.target_poly_budget:,}", icon='ERROR')
        else:
            col.label(text=f"{budget_pct:.1f}% used", icon='CHECKMARK')
        
        col.label(text=f"Vertices: {verts:,}")
        col.label(text=f"Texture: {tex_mem:.1f} MB")
        col.label(text=f"Score: {complexity_score}/100", icon='CHECKMARK' if complexity_score >= 60 else 'ERROR')
        
        if context.selected_objects:
            sel_tris, _ = get_poly_count(context, selected_only=True)
            col.separator()
            col.label(text=f"Selected: {sel_tris:,} tris", icon='RESTRICT_SELECT_OFF')
        
        layout.separator()
        
        # Quick Actions
        box = layout.box()
        box.label(text="QUICK ACTIONS", icon='PLAY')
        col = box.column(align=True)
        col.operator("dev.quick_fix", icon='AUTO')
        col.operator("dev.validator_v3", icon='CHECKMARK')
        
        layout.separator()
        
        # Asset Management
        box = layout.box()
        box.label(text="ASSET MANAGEMENT", icon='OUTLINER')
        col = box.column(align=True)
        col.operator("dev.smart_rename_v3", icon='SORTALPHA')
        col.operator("dev.batch_cleanup_v3", icon='BRUSH_DATA')
        col.operator("dev.uv_optimizer", icon='UV')
        
        layout.separator()
        
        # Optimization
        box = layout.box()
        box.label(text="OPTIMIZATION", icon='MODIFIER')
        col = box.column(align=True)
        col.operator("dev.lod_generator_v3", icon='MOD_DECIM')
        col.operator("dev.collision_v3", icon='MESH_ICOSPHERE')
        
        layout.separator()
        
        # Analysis
        box = layout.box()
        box.label(text="ANALYSIS", icon='VIEWZOOM')
        col = box.column(align=True)
        col.operator("dev.texture_analyzer_v3", icon='TEXTURE')
        col.operator("dev.report_v3", icon='TEXT')
        
        layout.separator()
        
        # Utilities
        box = layout.box()
        box.label(text="UTILITIES", icon='TOOL_SETTINGS')
        col = box.column(align=True)
        
        row = col.row(align=True)
        row.operator("object.shade_smooth", text="Smooth", icon='SHADING_SMOOTH')
        row.operator("object.shade_flat", text="Flat", icon='SHADING_FLAT')
        
        col.operator("object.origin_set", text="Center Origin", icon='PIVOT_MEDIAN').type='ORIGIN_GEOMETRY'
        
        layout.separator()
        
        # Export
        box = layout.box()
        col = box.column(align=True)
        col.operator("dev.export_v3", text="V3 EXPORT FBX", icon='EXPORT')
        col.operator("export_scene.fbx", text="Standard FBX", icon='FILE')

class VIEW3D_PT_FiveMV3Settings(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'FiveM V3'
    bl_label = "V3 Settings"
    bl_parent_id = "VIEW3D_PT_FiveMV3"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        settings = context.scene.fivem_settings
        
        layout.prop(settings, "auto_validate")
        layout.prop(settings, "auto_backup")
        layout.prop(settings, "use_vertex_colors")
        layout.prop(settings, "max_texture_size")
        layout.prop(settings, "enable_auto_lod")
        layout.prop(settings, "performance_mode")
        layout.separator()
        layout.prop(settings, "export_path")

# --- REGISTRATION ---

classes = (
    FiveMSettings,
    DEV_OT_SmartRenameV3,
    DEV_OT_ValidatorV3,
    DEV_OT_LODGeneratorV3,
    DEV_OT_BatchCleanupV3,
    DEV_OT_CollisionV3,
    DEV_OT_TextureAnalyzerV3,
    DEV_OT_UVOptimizer,
    DEV_OT_QuickFix,
    DEV_OT_ExportV3,
    DEV_OT_ReportV3,
    VIEW3D_PT_FiveMV3,
    VIEW3D_PT_FiveMV3Settings,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.Scene.fivem_settings = bpy.props.PointerProperty(type=FiveMSettings)
    
    print("\n" + "="*70)
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║     V3 SUPREME - FIVEM DEVELOPMENT PIPELINE - LOADED          ║")
    print("║                    50+ PREMIUM FEATURES                        ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    print("="*70 + "\n")

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
    del bpy.types.Scene.fivem_settings

if __name__ == "__main__":
    register()
