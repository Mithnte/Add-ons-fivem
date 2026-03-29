# 🔥 FiveM Development Pipeline V3 🔥

## 📖 COMPLETE DOCUMENTATION

### Version: 3.99.0
### Author: Bae & Dev Team
### Category: FiveM/GTA V Development

---

## 🎯 WHAT IS THIS?

**FiveM Development Pipeline V3 SUPREME** adalah Blender addon ULTIMATE untuk FiveM/GTA V asset development dengan **50+  features**. Script ini dibuat untuk memaksimalkan workflow development dan menghasilkan assets berkualitas tinggi yang optimized untuk FiveM server.

---

## ⚡ INSTALLATION

### Cara Install:

1. **Download** file `fivem_pipeline_v3_supreme.py`
2. Buka **Blender** (versi 3.6 atau lebih baru)
3. Pergi ke **Edit > Preferences > Add-ons**
4. Klik **Install...**
5. Pilih file `fivem_pipeline_v3_supreme.py`
6. **Centang checkbox** di samping "FiveM Development Pipeline V3 SUPREME"
7. Done! ✓

### Cara Akses:

- Tekan **N** di 3D Viewport
- Pilih tab **"FiveM V3"** di sidebar
- Semua tools ada di sana!

---

## 🚀 FITUR LENGKAP

### 📊 LIVE STATISTICS
- **Real-time Triangle Count** - Monitor poly count secara live
- **Budget Tracking** - Tracking apakah udah melebihi budget atau belum
- **Texture Memory Monitor** - Total memory usage dari semua texture
- **Complexity Score** - Skor kompleksitas scene (0-100)
- **Selected Object Stats** - Stats untuk object yang dipilih

### 🏷️ ASSET MANAGEMENT

#### 1. **V3 Smart Rename**
- **AI Auto-Detection** - Otomatis detect tipe object (vehicle/prop/weapon/etc)
- **8 Prefix Types**:
  - `prop_` - World props
  - `p_` - Ped accessories (clothing)
  - `v_` - Vehicle parts
  - `veh_` - Full vehicles
  - `lod_` - LOD meshes
  - `int_` - Interior props
  - `weap_` - Weapons
  - `col_` - Collision meshes
- **Quality Suffix** - Auto add _high/_med/_low based on poly count
- **Batch Renaming** - Rename multiple objects sekaligus

**Cara Pakai:**
```
1. Select objects yang mau di-rename
2. Klik "V3 Smart Rename"
3. Pilih prefix type atau enable "Auto-Detect"
4. Atur base name
5. Klik OK
```

#### 2. **V3 Geometry Validator**
- **8 Geometry Checks**:
  - N-Gons detection
  - Non-manifold geometry
  - Loose vertices
  - Degenerate faces
  - Zero-area faces
  - Missing UVs
  - Inverted normals
  - Non-uniform scale
- **Auto-Fix Mode** - Automatically fix issues
- **Detailed Report** - Comprehensive issue reporting

**Cara Pakai:**
```
1. Select objects (atau kosongkan untuk check semua)
2. Klik "V3 Geometry Validator"
3. Enable "Auto-Fix" jika mau langsung diperbaiki
4. Pilih check options
5. Klik OK
```

#### 3. **V3 Batch Cleanup**
- **7 Cleanup Operations**:
  - Remove doubles (merge vertices)
  - Recalculate normals
  - Delete loose geometry
  - Smart UV project
  - Apply scale
  - Add weighted normals
  - Limited dissolve (simplify edges)
- **Custom Parameters** - Merge distance, dissolve angle
- **Material Cleanup** - Auto remove unused materials

**Cara Pakai:**
```
1. Select objects
2. Klik "V3 Batch Cleanup"
3. Pilih operations yang mau dijalankan
4. Adjust parameters (merge distance, etc)
5. Klik OK
```

#### 4. **UV Optimizer**
- **Smart UV Packing** - Pack UV islands efficiently
- **Island Rotation** - Rotate for better packing
- **Average Island Scale** - Normalize island sizes
- **Custom Margin** - Control spacing between islands

### ⚡ OPTIMIZATION TOOLS

#### 5. **V3 LOD Generator**
- **4 Quality Presets**:
  - High Quality (50%, 25%, 12%)
  - Balanced (40%, 20%, 8%)
  - Performance (30%, 15%, 5%)
  - Ultra Performance (20%, 10%, 3%)
- **1-5 LOD Levels** - Generate multiple LOD levels
- **Smart Preservation**:
  - Preserve UVs
  - Preserve sharp edges
  - Preserve material boundaries
- **Automatic Naming** - Auto name as objectname_LOD1, _LOD2, etc

**Cara Pakai:**
```
1. Select high-poly objects
2. Klik "V3 LOD Generator"
3. Pilih quality preset
4. Set jumlah LOD levels
5. Enable preservation options
6. Klik OK
```

**Best Practices:**
- Gunakan **Balanced** untuk most cases
- Gunakan **Performance** untuk distant objects
- Gunakan **High Quality** untuk hero assets
- Generate 3 LOD levels untuk best results

#### 6. **V3 Collision Generator**
- **6 Collision Types**:
  - Convex Hull (best for complex shapes)
  - Bounding Box (fastest, simple box)
  - Decimated Mesh (simplified version)
  - Cylinder (for cylindrical objects)
  - Sphere (for round objects)
  - Capsule (for character collision)
- **Collision Collection** - Auto organize dalam collection terpisah
- **Visual Material** - Green wireframe material untuk visibility
- **GTA V Naming** - Automatic "col_" prefix

**Cara Pakai:**
```
1. Select objects yang butuh collision
2. Klik "V3 Collision Generator"
3. Pilih collision type
4. Enable "Add to Collision Collection"
5. Klik OK
```

**Recommendations:**
- **Convex Hull** - Default choice, good for most objects
- **Bounding Box** - Untuk simple furniture/props
- **Decimated** - Untuk complex shapes yang butuh detail
- **Cylinder** - Untuk poles, barrels, columns
- **Sphere** - Untuk balls, wheels
- **Capsule** - Untuk character collisions

### 📊 ANALYSIS TOOLS

#### 7. **V3 Texture Analyzer**
- **Memory Calculation** - Total texture memory usage
- **Resolution Report** - Show texture resolutions
- **Optimization Suggestions** - Suggest downsizing oversized textures
- **Top Textures** - Show largest textures first
- **Console Report** - Detailed console output

**Cara Pakai:**
```
1. Klik "V3 Texture Analyzer"
2. Enable "Suggest Optimizations"
3. Klik OK
4. Check console output (Window > Toggle System Console)
```

**Reading the Report:**
```
✓ = Texture size OK (<4MB)
⚠ = Texture oversized (>4MB)
```

#### 8. **V3 Generate Report**
- **Comprehensive Scene Analysis**
- **Performance Rating** - EXCELLENT/GOOD/NEEDS OPTIMIZATION
- **Budget Status** - Over/under poly budget
- **Texture Analysis** - Memory usage breakdown
- **Export to JSON** - Machine-readable format
- **Console Report** - Beautiful formatted output

### 🔧 QUICK TOOLS

#### 9. **V3 Quick Fix All**
- **One-Click Optimization** - Fix all common issues
- **Auto Operations**:
  - Apply scale
  - Remove doubles
  - Delete loose geometry
  - Recalculate normals
  - Limited dissolve
  - Material cleanup
- **Scene-Wide** - Works on all objects

**Cara Pakai:**
```
1. Klik "V3 Quick Fix All"
2. Wait for processing
3. Done! ✓
```

**Use Cases:**
- Before export
- After importing models
- Quick scene cleanup
- Before validation

### 📦 EXPORT SYSTEM

#### 10. **V3 Export FBX**
- **Optimized Settings** - Pre-configured untuk FiveM/GTA V
- **Auto Backup** - Backup .blend file before export
- **Validation** - Warn jika poly count tinggi
- **Export Logging** - JSON log dengan timestamp
- **GTA V Axis** - Correct axis orientation (-Z forward, Y up)

**Cara Pakai:**
```
1. Select objects untuk export
2. Klik "V3 Export FBX"
3. Pilih lokasi save
4. Enable/disable options
5. Klik Export
```

**Export Settings:**
```
- Axis: Forward=-Z, Up=Y (GTA V standard)
- Apply Modifiers: YES
- Smooth Type: FACE
- Tangent Space: YES
```

---

## ⚙️ SETTINGS

### Global Settings (di Settings Panel):

1. **Project Name** - Nama project FiveM
2. **Poly Budget** - Target poly budget (default: 50,000)
3. **Optimization Level** - Quality/Balanced/Performance
4. **Auto Validate** - Auto validate sebelum save
5. **Auto Backup** - Auto backup sebelum major operations
6. **Use Vertex Colors** - Enable vertex color workflow
7. **Max Texture Size** - Maximum texture resolution
8. **Enable Auto LOD** - Auto generate LODs on export
9. **Performance Mode** - Enable performance optimizations
10. **Export Path** - Default export directory

---

## 📈 WORKFLOW RECOMMENDATIONS

### Typical Workflow:

1. **Import/Create Model**
2. **V3 Smart Rename** - Rename dengan proper naming
3. **V3 Quick Fix All** - Quick cleanup
4. **V3 Geometry Validator** - Validate dengan auto-fix
5. **V3 Batch Cleanup** - Deep cleanup dengan custom settings
6. **UV Optimizer** - Optimize UV layout
7. **V3 LOD Generator** - Generate LOD levels
8. **V3 Collision Generator** - Create collision meshes
9. **V3 Texture Analyzer** - Check texture usage
10. **V3 Generate Report** - Final quality check
11. **V3 Export FBX** - Export untuk FiveM

### Quality Checklist:

✅ **Geometry:**
- [ ] No N-Gons
- [ ] No loose vertices
- [ ] No non-manifold geometry
- [ ] Normals facing correct direction
- [ ] Scale applied (1.0, 1.0, 1.0)

✅ **UVs:**
- [ ] UV map exists
- [ ] UVs properly packed
- [ ] No overlapping UVs (unless intentional)

✅ **Textures:**
- [ ] Texture size reasonable (<4MB per texture)
- [ ] Resolution appropriate (2K max untuk most cases)
- [ ] No unused textures

✅ **Optimization:**
- [ ] Poly count within budget
- [ ] LOD levels generated
- [ ] Collision mesh created
- [ ] Materials optimized

✅ **Naming:**
- [ ] Proper GTA V prefix
- [ ] Sequential numbering
- [ ] No special characters
- [ ] Lowercase preferred

---

## 🎯 PERFORMANCE TARGETS

### Recommended Poly Budgets:

**Props:**
- Small props: 500-2,000 tris
- Medium props: 2,000-8,000 tris
- Large props: 8,000-20,000 tris

**Vehicles:**
- Exterior: 30,000-80,000 tris
- Interior: 15,000-30,000 tris
- Total: 45,000-110,000 tris

**Weapons:**
- First person: 8,000-15,000 tris
- Third person: 2,000-5,000 tris

**Peds/Characters:**
- Body: 10,000-25,000 tris
- Accessories: 500-2,000 tris per item

### Texture Guidelines:

**Resolution:**
- Props: 512x512 to 1024x1024
- Vehicles: 1024x1024 to 2048x2048
- Characters: 1024x1024 to 2048x2048
- Weapons: 512x512 to 1024x1024

**Formats:**
- Diffuse/Albedo: RGB (no alpha jika tidak perlu)
- Normal Maps: RGB
- Roughness/Metallic: Grayscale atau combined

---

## 🐛 TROUBLESHOOTING

### Common Issues:

**"V3: No objects selected"**
- Solution: Select objects first sebelum run operator

**"High poly count warning"**
- Solution: Use LOD Generator atau Batch Cleanup untuk reduce

**"Textures over 4MB"**
- Solution: Use Texture Analyzer untuk identify, resize di image editor

**"Non-manifold geometry detected"**
- Solution: Use Geometry Validator dengan Auto-Fix enabled

**Export fails**
- Solution: Check console untuk error details, validate geometry first

### Performance Issues:

**Addon slow pada scene besar:**
- Enable "Performance Mode" di settings
- Reduce "Max Texture Size"
- Work dengan selection instead of full scene

---

## 💡 TIPS & TRICKS

### Pro Tips:

1. **Use Collections** - Organize assets dalam collections (Props, Vehicles, Collision)
2. **Name Early** - Rename objects di awal workflow
3. **Validate Often** - Run validator setelah major changes
4. **LOD First** - Generate LODs sebelum materials
5. **Backup Always** - Enable auto backup
6. **Console is Your Friend** - Check console untuk detailed info
7. **Batch Operations** - Select multiple objects untuk efficiency
8. **Test In-Game** - Always test dalam FiveM sebelum finalize

### Keyboard Shortcuts:

- **N** - Toggle sidebar (access V3 panel)
- **A** - Select all
- **Alt+A** - Deselect all
- **H** - Hide selected
- **Alt+H** - Unhide all

---

## 📝 CHANGELOG

### V3.99.0 - SUPREME EDITION
- ✨ 50+ premium features
- 🚀 AI-powered object type detection
- 📊 Advanced texture analyzer
- ⚡ Performance optimizations
- 🎯 Comprehensive validation
- 📈 Real-time complexity scoring
- 🔧 One-click quick fix
- 📦 Optimized export system

---

## 🤝 SUPPORT

### Need Help?

1. Check documentation (this file)
2. Check console output untuk detailed errors
3. Use "V3 Generate Report" untuk diagnostics
4. Validate geometry dengan auto-fix

### Feature Requests:

Script ini sudah COMPLETE dengan 50+ features covering semua aspek FiveM development!

---

## ⚖️ LICENSE

Free to use untuk FiveM development.
Created by Premium Dev Team.

---

## 🎉 CONCLUSION

**FiveM Development Pipeline V3 SUPREME** adalah ultimate solution untuk FiveM asset development. Dengan 50+ premium features, AI-powered detection, dan comprehensive validation, script ini akan dramatically improve workflow dan menghasilkan high-quality, optimized assets untuk FiveM server.

### Key Benefits:

✅ **Save Time** - Automate repetitive tasks
✅ **Better Quality** - Professional validation
✅ **Optimized Performance** - Built-in optimization tools
✅ **Easy to Use** - Intuitive interface
✅ **Complete Solution** - Everything you need dalam one addon

**Happy Developing! 🔥**

---

**Version:** 3.99.0 
**Last Updated:** 2026  
**Developed with Bae for FiveM Community**
