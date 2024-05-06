import copy

import numpy as np
import os
from slam import io
from slam import differential_geometry
from slam import vertex_voronoi
from slam import texture
from slam import curvature
import slam.plot as splt

from sandbox import watershed

def display_watershed():
    main_path = "/home/INT/leroux.b/Documents/Subj0001/guillaume/"
    mesh = io.load_mesh(os.path.join(main_path, "example_mesh.gii"))
    filename = "labels_bis.gii"
    tex_path = os.path.join(main_path, filename)

    tex = io.load_texture(tex_path)
    visb_sc = splt.visbrain_plot(
        mesh=mesh,
        tex=tex.darray[0],
        caption="Watershed",
        cblabel="Watershed",
    )
    visb_sc.preview()

def execution():

    main_path = "/home/INT/leroux.b/Documents/Subj0001/guillaume/"
    mesh_path = os.path.join(main_path, "example_mesh.gii")
    mesh = io.load_mesh(mesh_path)

    # curv = io.load_texture(main_path + "curv.gii")

    """dpf_tex = io.load_texture(main_path + "dpf.gii")
    vert_voronoi = np.load(main_path + "vert_voronoi.npy")"""

    # Compute the curvature
    print("\n\tComputing the curvature\n")
    PrincipalCurvatures, PrincipalDir1, PrincipalDir2 = curvature.curvatures_and_derivatives(
        mesh)
    mean_curv = 0.5 * (PrincipalCurvatures[0, :] + PrincipalCurvatures[1, :])

    curv = texture.TextureND(PrincipalCurvatures)
    io.write_texture(curv, os.path.join(main_path, "curv.gii"))

    # Compute the DPF and save it
    print("\n\tComputing the DPF\n")
    dpf = differential_geometry.depth_potential_function(mesh, mean_curv, [0.03])
    dpf_tex = texture.TextureND(darray=dpf[0])
    io.write_texture(dpf_tex, os.path.join(main_path, "dpf.gii"))

    mask = np.zeros(dpf_tex.shape[0])
    labels, pitsKept, pitsRemoved, ridgePoints, parent = watershed.watershed(mesh, "", dpf_tex.darray, mask, 0, 0)

    io.write_texture(texture.TextureND(darray=labels.flatten()), os.path.join(main_path, "labels_bis.gii"))

    """
    # Compute Voronoi's vertex and save it
    print("\n\tComputing Voronoi's vertex\n")
    vert_voronoi = vertex_voronoi.vertex_voronoi(mesh)
    # np.save(main_path + "vert_voronoi.npy", vert_voronoi)
    
    print("\n\tComputing the Fiedler geodesic length and surface area\n")
    mesh_area = np.sum(vert_voronoi)
    (mesh_fiedler_length, field_tex) = differential_geometry.mesh_fiedler_length(mesh, dist_type="geodesic")
    min_mesh_fiedler_length = min(mesh_fiedler_length)  # ?
    
    mask = np.zeros(dpf_tex.shape[0])
    
    thresh_dist = 20
    thresh_ridge = 1.5
    thresh_area = 50
    group_average_Fiedler_length = 238.25 if side == "right" else 235.95
    group_average_surface_area = 91433.68 if side == "right" else 91369.33
    
    thresh_dist *= min_mesh_fiedler_length / group_average_Fiedler_length
    thresh_area *= mesh_area / group_average_surface_area
    
    
    # Future step
    
    print('\n\tComputing the watershed with distance and ridge criteria for basins merging')
    labels_1, pitsKept_1, pitsRemoved_1, ridgePoints, parent_1 = watershed.watershed(mesh, vert_voronoi, dpf[0], mask,
                                                                                     thresh_dist, thresh_ridge)
    labels, infoBasins, pitsKept, pitsRemoved_2, parent = watershed.areaFiltering(mesh, vert_voronoi, labels_1,
                                                                                  pitsKept_1, parent_1, thresh_area)
    pitsRemoved = pitsRemoved_1 + pitsRemoved_2
    
    # texture of basins
    labels_tex = texture.TextureND(labels)
    io.write_texture(labels_tex, main_path + "label_tex.gii")
    
    # texture of pits
    atex_pits = np.zeros((len(labels), 1))
    for pit in pitsKept:
        atex_pits[pit[0]] = 1
    pits_tex = texture.TextureND(atex_pits)
    io.write_texture(pits_tex, main_path + "pits_tex_tex.gii")
    
    # texture of noisy pits
    atex_noisypits = np.zeros((len(labels), 1))
    for pit in pitsRemoved:
        atex_noisypits[pit[0]] = 1
    noisy_pits_tex = texture.TextureND(atex_noisypits)
    io.write_texture(noisy_pits_tex, main_path + "noisy_pits_tex.gii")
    
    # texture of ridges
    atex_ridges = np.zeros((len(labels), 1))
    for ridge in ridgePoints:
        atex_ridges[ridge[2]] = 1
    ridges_tex = texture.TextureND(atex_ridges)
    io.write_texture(ridges_tex, main_path + "rigdes_tex.gii")
    """


if __name__ == "__main__":
    execution()
    display_watershed()