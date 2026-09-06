# Depth Vision Sensors: Technological Evolution, Enabling Algorithms, and Applications in Mechatronic Systems

Bo Zhang1,2 | Hongchao Cui1,2

1 School of Mechanical, Electronic and Control Engineering, Beijing Jiaotong University, Beijing, China
2 Beijing Key Laboratory of Flow and Heat Transfer of Phase Changing in Micro and Small Scale, Beijing Jiaotong University, Beijing, China

**Corresponding author: Hongchao Cui (hccui@bjtu.edu.cn)**

## Abstract

Active depth vision sensors have become a standard perception front-end in mechatronic systems, including industrial robots, indoor mobile platforms, and unmanned aerial vehicles (UAVs). Unlike passive stereo or monocular depth estimation, structured light, time-of-flight (ToF), and solid-state light detection and ranging (LiDAR) emit controlled illumination and recover metric range with less dependence on scene texture. This review follows a hardware-centered narrative. First, we summarize the operating principles, representative devices, and reported operating envelopes of the three main active modalities. Second, we review the algorithms that convert raw depth into usable estimates: denoising and completion, multi-sensor fusion, visual-inertial-depth odometry, and geometric-semantic mapping. Third, we examine four application families in which the sensing modality is a first-order design choice: industrial inspection and bin picking, indoor mobile robots, UAVs, and collaborative robots. Remaining barriers are organized around sunlight and material sensitivity, compute and power, calibration, and interface fragmentation, together with emerging directions such as event-based depth, on-sensor inference, and photonic beam steering. The paper is intended as a compact map from sensor physics to system function for mechatronic designers, rather than a substitute for modality-specific hardware surveys.

Keywords: depth vision sensors; mechatronic systems; structured light; time-of-flight; solid-state LiDAR; SLAM; sensor fusion; collaborative robots

## 1. Introduction

Autonomous mobile robots, flexible manufacturing cells, and small UAVs all require a timely geometric model of the workspace [1,2,3,4]. Among perception options, vision remains attractive because it is non-contact, relatively inexpensive, and information-dense. Two-dimensional cameras supply appearance. Depth vision adds metric range, which simplifies obstacle clearance, grasp planning, and map scale. In a mechatronic system that coupling is not cosmetic: the same millimetre that is harmless in a visualization can be the difference between a successful insertion and a jammed assembly, or between a UAV standoff and a girder strike.

This review is restricted to active depth vision: sensors that illuminate the scene with a controlled optical source and recover three-dimensional geometry from the returned light. The main families are structured light and active stereo, continuous-wave and pulsed ToF cameras, and solid-state LiDAR [5,6,7,8,9,10]. We contrast them with passive stereo and learning-based monocular depth, which rely on ambient texture or data-driven priors [11,12,13]. Passive methods have improved rapidly, but active sensors remain the default in many deployed mechatronic systems because they provide dense or semi-dense metric depth on weakly textured surfaces and under changing indoor lighting [4,14,15].

The 2010 Microsoft Kinect showed that dense indoor depth could be obtained at consumer cost [14,16]. That device, and the algorithms built on it, moved RGB-D mapping and human pose estimation out of specialized laboratories [17,18,19]. Subsequent products reduced size and power (mobile ToF and active-stereo modules) and then extended range (solid-state LiDAR), which changed the set of machines that could carry a depth sensor [9,10,20,21].

Several surveys already cover pieces of this landscape (Table 1). Lock-in ToF cameras [7], ToF range imaging more broadly [8,22,23], structured-light metrology [5,6], comparative RGB-D tests [4,24], visual SLAM [1,25,26,27], event cameras [28], and LiDAR hardware [9,10,29,30] are all better treated in those sources than they can be in one paper. What is still useful, and what this paper attempts, is not another first-principles optics tutorial. It is a system-level map that answers a design question: which physical generation of depth sensor made which mechatronic function practical, and which residual errors still dominate in the field.

*Table 1. Closest prior surveys and the slice added here. This paper is complementary, not a replacement.*

| Prior survey | Main focus | What a mechatronic designer still has to assemble |
| --- | --- | --- |
| Foix et al.; Horaud et al. [7,8] | ToF camera physics and calibration | How iToF/dToF sit next to SL and LiDAR on a robot |
| Zhang; Geng [5,6] | Structured-light metrology | When a fringe scanner is the wrong robot sensor |
| Halmetschlager-Funek et al. [4] | Empirical RGB-D ranking | Estimator and application consequences |
| Cadena et al.; later V-SLAM surveys [1,26] | SLAM algorithms | Which depth front-end the estimator assumes |
| Ho et al.; Roriz et al. [9,10] | Solid-state / automotive LiDAR | Indoor RGB-D and factory cells |
| Gallego et al. [28] | Event cameras | When event depth is worth the stack change |

### 1.1 Scope and review method

The paper is a narrative review, not a PRISMA systematic review. We screened IEEE Xplore, Scopus, Web of Science, and major publisher libraries for English-language work from approximately 2001 to early 2025. Search phrases combined structured light, time-of-flight camera, RGB-D, solid-state LiDAR, depth completion, visual-inertial odometry, RGB-D SLAM, bin picking, collaborative robot, and UAV obstacle avoidance. Priority was given to seminal hardware and calibration papers, widely cited surveys, comparative evaluations that report quantitative error, and application studies in which the depth modality is specified. Product datasheets are used only as supporting context and are not treated as peer-reviewed evidence. Mechanical spinning LiDAR is discussed only as a baseline for solid-state designs. Biomedical and purely cinematic uses of depth cameras are outside the scope.

### 1.2 Contributions and organization

The paper makes four modest contributions. First, it compares structured light, active stereo, iToF, dToF, and solid-state LiDAR by principle, reported range and error, and typical mechatronic role. Second, it links raw depth artifacts to the estimation layers that machines actually run. Third, it organizes applications by sensing requirement rather than by market category. Fourth, it separates mitigations that already ship from ideas that remain research. Section 2 reviews hardware. Section 3 reviews enabling algorithms. Section 4 reviews applications. Section 5 discusses open problems and outlook. Section 6 concludes.

## 2. Technological evolution of depth vision sensors

A useful first cut is the operating envelope: the combination of range, spatial resolution, ambient-light tolerance, size, and cost that a machine can actually use. Figure 1 summarizes the three families that dominate current mechatronic designs.

![](figures/fig1_operating_envelopes.png)

*Figure 1. Typical operating envelopes of structured light / active stereo, ToF cameras, and solid-state LiDAR, together with the mechatronic roles that follow from those envelopes. Bounds are qualitative summaries of the literature in Table 2, not guarantees for a particular device.*

### 2.1 Structured light and active stereo

Structured-light sensors project a known pattern (dots, stripes, or time-varying fringes) and recover depth by triangulation between the projector and one or more cameras [5,6]. If f is the focal length, B the baseline, and d the observed disparity, the pinhole relation is Z = fB/d. Error in disparity therefore grows into a range error that increases approximately with Z squared [14]. Industrial systems usually prefer sequential Gray-code plus phase-shifting fringes because the absolute unwrapping is robust and the phase gives sub-pixel disparity [5,6]. Fourier-transform profilometry trades some robustness for a single-shot capture, which matters on moving parts. Industrial fringe-projection systems exploit this geometry at short range and can reach tens of micrometres to sub-millimetre accuracy on cooperative surfaces [5]. The price of that accuracy is a controlled standoff, a cooperative (or at least non-specular) surface, and a workspace that fits the calibrated volume.

Consumer devices traded metrology-grade projectors for a static pseudo-random speckle and on-chip matching. Kinect v1 is the canonical example: a near-infrared (NIR) projector, an infrared camera, and a colour camera. Khoshelham and Elberink showed that its random depth error grows from a few millimetres near the sensor to about 4 cm near 5 m, while axial point spacing can reach about 7 cm at that range [14]. Those numbers explain both the success of KinectFusion-style indoor reconstruction [17,18] and the unsuitability of the same sensor as an outdoor navigation camera.

Active stereo keeps triangulation but replaces a coded single-camera pattern with a stereo pair plus a texture projector. Intel RealSense R200/D400-class cameras follow this route [20]. Because matching runs on two infrared images, the system can still return depth when the projector is weak or switched off, which improves outdoor behaviour relative to first-generation speckle sensors [4,20]. The cost is compute for stereo matching and a stronger dependence on calibration [11,20]. Indoor tests across structured-light, active-stereo, and ToF units confirm that no single consumer camera dominates bias, precision, lateral noise, lighting, and multi-sensor interference at once [4,24].

### 2.2 Time-of-flight cameras and mobile miniaturization

A ToF pixel estimates range from the travel time of light. Indirect ToF (iToF; lock-in or continuous-wave) measures the phase shift of a modulated source [7,31]. For a modulation frequency f_m the unambiguous range is on the order of c/(2 f_m); a typical 30 MHz tone wraps near 5 m, which is why multi-frequency operation appears on industrial iToF cameras [7,8]. Direct ToF (dToF) timestamps a short pulse, often with single-photon avalanche diode (SPAD) arrays and time-to-digital converters [8,21,32]. iToF became practical in compact cameras because a single illuminator and a single sensor replace a precision stereo baseline [7,15]. Reported indoor working distances for consumer iToF, including Kinect v2, are typically 0.5-4.5 m [15,33,34]. Side-by-side studies of Kinect v1 and v2 show that the ToF unit reduced some structured-light artifacts (texture dependence, multi-device interference) while introducing others (multipath in corners, flying pixels, wiggling) [15,33,34]. Sunlight, multipath, and flying pixels remain first-order limitations [15,33,35].

The same physics explains the mobile-ToF wave of the 2010s. A phase camera does not need a wide mechanical baseline, so it fits a phone or an embedded robot head. Early mobile iToF modules were lower in spatial resolution than structured light but more convenient at 2-5 m for augmented reality and coarse scene layout [8,21]. dToF SPAD arrays later improved ambient-light rejection and power per unit of range, at the expense of histogram memory and, often, spatial resolution [21]. Gyongy, Dutton, and Henderson review the dToF signal chain and show why on-chip histogram compression, not only detector quantum efficiency, now limits array size [21].

### 2.3 Solid-state LiDAR and the long-range shift

Once the task leaves the room (warehouse aisles, yards, roads, bridge girders) consumer RGB-D cameras run out of photons and out of unambiguous range. Mechanical spinning LiDAR already solved long-range ranging. Solid-state and semi-solid designs try to keep that range while removing a bulky rotator [9,10,29,30]. MEMS mirrors scan a laser with a small moving mass and are the most commercially mature semi-solid option. Flash LiDAR illuminates a patch at once and is closer to a ToF camera, with range and resolution set by peak power and pixel count. Optical phased arrays and metasurface beam steerers aim at a fully solid-state scanner [36,37,38,39,40]. Large-scale silicon photonic arrays and MEMS-on-photonics demonstrators show that chip-scale beam steering is no longer only a laboratory sketch [38,40]. For mechatronic integration the practical facts are simpler: solid-state units are smaller and potentially more robust to vibration, but they are still sparse compared with RGB-D, still expensive at automotive grade, and still require careful time synchronization with cameras and IMUs [10,29,41]. Automotive surveys also stress eye-safety, rain/fog backscatter, and the need for a perception stack that does not treat a sparse cloud as if it were a Kinect frame [10,29].

Table 2 collects order-of-magnitude figures reported in the literature. Values are typical envelopes, not guarantees for a particular serial number. Two design rules follow. First, do not treat "depth camera" as one specification: a sensor that is excellent for bin picking is usually the wrong sensor for a 30 m warehouse aisle. Second, hardware generations did not replace one another; they split the operating envelope. Structured light still wins close-range accuracy. ToF wins compactness at room scale. Solid-state LiDAR wins range. Mechatronic architectures increasingly carry more than one of them.

A practical selection sequence used in many robot shops is: write down the minimum and maximum range, the worst lighting, the worst surface, the allowed mass and watts, and the safety integrity level. Only then open a catalogue. Indoor rooms with matte walls still suit RGB-D [4,14,20]. Fixed cells with metal parts still suit industrial structured light [5]. Yards and roads still suit LiDAR, usually fused with cameras [10,41,42]. If two of those worlds appear on one machine, budget two sensors and a calibration procedure, not a single "universal" depth camera.

Three short examples make the same point. A bin-picking cell with a 1.2 m standoff and oily steel parts should start from industrial structured light, a 6-DoF pose estimator, and a compliant grasp, not from a 100 m LiDAR [5,43,44]. An indoor delivery base that must see a pallet toe and a person in a corridor should start from a wide RGB-D camera plus a two-dimensional safety LiDAR and a visual-inertial estimator [20,45,46]. A bridge-inspection UAV that must hold a 5-15 m standoff in wind should start from a lightweight solid-state ranger, an IMU, and a compact RGB inspector, and should not expect a phone-class ToF module to carry the ranging load [2,9,47].

*Table 2. Representative operating envelopes of active depth sensors used in mechatronics. Numbers are typical ranges reported in peer-reviewed evaluations or hardware surveys; product variants differ.*

| Family | Principle | Typical usable range | Reported depth error (order) | Spatial sampling | Main field weakness | Typical role | Sources |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Structured light (consumer) | Static-pattern triangulation | 0.5-4 m | mm near field; ~4 cm random error near 5 m (Kinect v1) | Dense VGA-class | Sunlight; shiny or absorbing surfaces | Indoor mapping, HRI prototypes | [4,14,15] |
| Fringe / industrial SL | Phase-shifting triangulation | 0.1-2 m (setup-dependent) | tens of um to sub-mm | Very dense | Workspace size; ambient light | In-line metrology, bin picking | [5,6] |
| Active stereo | IR stereo + texture projector | 0.2-10 m (best ~0.3-3 m) | cm-level, lighting-dependent | Dense HD-class | Calibration; compute; texture holes | Indoor / semi-outdoor robots | [4,20] |
| iToF camera | CW phase | 0.5-5 m | cm-level; multipath bias | Dense QVGA-VGA | Multipath; sunlight; flying pixels | Mobile robots, mid-range HRI | [7,8,15,33] |
| dToF SPAD | Pulsed photon timing | ~1-10 m consumer; longer if laser-class | cm-level; better ambient rejection than iToF | Often coarser | Histogram memory; pile-up | AR, short-range robots | [21,32] |
| Solid-state / MEMS LiDAR | Scanned or flash ToF | 10-200+ m | few cm (range- and target-dependent) | Sparse points | Cost; weather; boresight | Outdoor AMR, UAV, vehicle | [9,10,29] |

## 3. Enabling technologies: from raw depth to a state estimate

Raw depth is not a pose, a mesh, or a grasp. This section reviews the software layers that mechatronic systems insert between the sensor and the controller.

### 3.1 Depth data processing and enhancement

Consumer and automotive depth images share a small set of artifacts: impulse noise, invalid pixels (holes) on occlusions, black or specular surfaces, flying pixels on depth edges, and ToF multipath [4,7,15]. Classical spatial median filters and temporal averaging remain the first firmware line of defence. When a registered RGB image is available, joint bilateral or guided filtering uses colour edges to protect object boundaries while smoothing planar interiors [48]. These filters are cheap enough for embedded GPUs. They do not invent missing geometry.

Depth completion does. Early methods inpainted by diffusion or multi-view geometry. Learning-based completion trained on RGB-D or RGB-plus-sparse-LiDAR pairs now dominates the literature [12,13,49,50,51,52,53]. Eigen et al. showed that a multi-scale network can predict depth from a single RGB image [12]; later residual and self-supervised models reduced the need for dense ground truth [13,50,51]. Indoor work still leans on NYU-Depth v2-style labelled apartments [49]. Outdoor work leans on KITTI-style projected LiDAR, which is sparse and biased toward the road plane [52]. For that setting, Uhrig et al. introduced sparsity-invariant convolutions [52], and Ma and Karaman showed that even a few hundred metric samples plus RGB yield a dense metric map [53]. Later non-local and transformer architectures improve large holes by using long-range context, at a cost that still challenges small onboard computers [54]. A mechatronic reading of these papers is that completion is a good virtual sensor for visualization and mid-level planning, and a bad sole input to a safety-rated stop.

Table 3 rates common artifacts by industrial maturity. The important systems point is that learning-based completion is not yet a drop-in safety sensor: it can look plausible while being metrically wrong on transparent, thin, or never-seen objects.

*Table 3. Common depth artifacts and the maturity of current mitigations.*

| Artifact | Dominant cause | Typical mitigation | Maturity |
| --- | --- | --- | --- |
| Impulse noise | Low SNR, scattering | Median filter; temporal averaging | Mature (on-chip / firmware) |
| Holes / invalid pixels | Occlusion, IR absorption, specularity, out-of-range | RGB-guided completion; multi-view fusion | Emerging for real-time embedded use |
| Flying pixels / motion blur | Finite integration time | Shorter exposure; IMU-aided deblur; event sensing | Mixed: IMU fusion common; event methods still research |
| Multipath (ToF) | Indirect returns in corners and shiny rooms | Multi-frequency modulation; coded ToF; model-based subtraction | Maturing on high-end iToF; still hard on cheap single-frequency units [7,35] |
| Sunlight saturation | Ambient NIR swamping the source | Narrow-band filters; higher peak power; dToF / LiDAR; radar fill-in | Partly solved at LiDAR-class power; unsolved for cheap RGB-D outdoors [4,15] |

### 3.2 Sensor fusion and state estimation

A depth camera alone is a poor navigation sensor: it is biased, partially observed, and asynchronous with the actuators. Fusion with an inertial measurement unit (IMU), wheel odometry, and/or a colour camera is therefore the default architecture on mobile robots and UAVs (Figure 2).

![](figures/fig2_sensor_fusion_stack.png)

*Figure 2. A typical estimation stack on a mobile robot. Depth is one residual source among several. The optional dense or semantic layer is expensive and is often omitted on large-scale outdoor maps.*

Loose coupling treats each sensor as a black-box pose or twist and fuses them in an extended or unscented Kalman filter. The implementation is modular and cheap; the estimate is statistically suboptimal and cannot correct inner calibration errors [55]. Tight coupling, as in keyframe visual-inertial odometry (VIO), jointly optimizes visual residuals and IMU preintegration in a sliding window [56,57,58,59]. Adding metric depth yields visual-inertial-depth odometry: depth removes the monocular scale-gauge ambiguity and supplies geometric constraints in low-texture rooms where VIO would otherwise drift or fail [1,17,58].

Dense RGB-D fusion, from KinectFusion through ElasticFusion and BundleFusion, maintains a truncated signed distance function (TSDF) or surfel map for close-range interaction [17,60,61]. The KinectFusion loop is still the mental model: track the live depth against the model, integrate the new frame into a volume, and raycast a synthetic depth for the next track [17,18]. ElasticFusion dropped the explicit pose graph in favour of dense deformation; BundleFusion restored global consistency with on-the-fly reintegration [60,61]. Those maps are excellent for a tabletop and expensive for a warehouse. Graph-based SLAM adds loop closures so that local odometry does not accumulate without bound [1,55]. RGB-D SLAM systems and the TUM RGB-D benchmark made this stack reproducible [19,62,63]. Later systems (ORB-SLAM2/3, Kimera) combine sparse or semi-dense tracking with optional metric-semantic mapping and multi-robot extensions [46,64,65,66]. ORB-SLAM3 in particular folded visual-inertial and multi-map operation into a library that many robot teams actually run [46]. Direct methods such as LSD-SLAM showed that dense photometric residuals can replace sparse features when exposure is well modelled [67]. Visual-LiDAR fusion surveys document the complementary pair used outdoors: cameras for semantics and texture, LiDAR for metric structure and lighting invariance [41,42].

Point-cloud infrastructure (PCL, iterative closest point, OctoMap, Voxblox) determines whether these estimators can run online on a real chassis [68,69,70,71]. For control engineers the interface that matters is usually a pose with covariance plus a costmap, not a research SLAM paper. Table 4 compares the fusion patterns that those libraries usually sit under.

*Table 4. Fusion patterns used in mechatronic state estimation.*

| Pattern | Typical inputs | Estimator | Output | Fits | Main cost |
| --- | --- | --- | --- | --- | --- |
| Loose coupling | Depth pose, IMU, wheels | EKF / UKF | 6-DoF pose | Structured indoor bases | Easy, less accurate |
| Tight VIO / VIDO | RGB, IMU, depth | Sliding-window BA | Pose + sparse map | Drones, AR, agile bases | Calibration and CPU |
| Dense RGB-D | Depth + RGB | TSDF / surfels | Mesh or volume | Manipulation, inspection | Memory and scale |
| Pose-graph SLAM | Any odometry + loops | Graph optimization | Globally consistent map | Buildings, multi-floor | Place recognition |
| Visual-LiDAR | Camera + LiDAR + IMU | Tight or loosely fused SLAM | Large-scale metric map | Outdoor AMR / UAV | Sync and extrinsics [41] |

### 3.3 From geometry to semantics

Once a metric cloud exists, the next questions are what the object is and where the robot may go. Classical 3D detectors used hand-crafted histograms. Current networks consume raw points, voxels, or range images [54,72,73]. Semantic segmentation labels every point; instance segmentation separates two chairs of the same class. RGB remains useful for texture and class priors; depth remains useful for scale and occlusion. Pose-estimation benchmarks such as BOP and methods such as PoseCNN made 6-DoF object pose a measurable industrial problem rather than a one-off demonstration [74,75].

Beyond labels, mechatronic systems care about affordances: surface normals and curvature for grasp stability, traversable floor versus negative obstacles, and dynamic scene graphs that persist over time [44,65,66]. These layers are not unique to depth sensors, but they become cheaper when scale is observed rather than inferred. In dynamic scenes, geometric SLAM without semantics remains brittle; recent surveys document the shift toward semantic and robust dynamic SLAM [27,76].

## 4. Applications in mechatronic systems

The same sensor physics appears as different requirements once a machine has a job. This section organizes applications by the depth property that is actually spent.

### 4.1 Industrial automation and precision manufacturing

Bin picking and unstructured part handling spend spatial resolution and short-range accuracy. A sensor above the bin produces a point cloud; a pose estimator returns a 6-DoF grasp; a compliant gripper absorbs the residual error [43,44,74,75,77,78]. Grasp-from-point-cloud methods (GPD, Dex-Net and their successors) showed that a depth image plus analytic or learned grasp scores can propose suction or parallel-jaw contacts without a full CAD model of every SKU [44,77]. When the part identity is known, multi-view pose networks of the Amazon Picking Challenge generation, and later PoseCNN-style estimators scored on BOP, turn the same cloud into a 6-DoF object pose [74,75,78]. The first Amazon Picking Challenge made the systems nature of this problem obvious: teams that treated perception, planning, and gripping as separately optimized modules underperformed relative to tightly integrated stacks, and suction often beat anthropomorphic hands [43]. Structured light and laser triangulation still dominate when parts are metallic, overlapping, and closer than about two metres [5,43]. RGB is typically fused for class identity; force and torque close the last millimetres.

In-line metrology spends repeatability and speed. A fringe-projection or ToF snapshot is compared with a computer-aided design (CAD) model. Fringe systems own the micrometre-to-sub-millimetre band [5,6]. ToF cameras are used when the assembly is large and a few millimetres of error are acceptable, because a full-field frame arrives without a scanning gantry [7,8]. Vibration of the line is then a fusion problem (encoders and triggers), not only an optics problem.

Automated guided vehicles (AGVs) and autonomous mobile robots (AMRs) spend field of view and vertical coverage. A two-dimensional safety LiDAR sees a plane; a wide RGB-D camera or solid-state LiDAR sees pallets, overhangs, and people who lean into the aisle [4,42,45]. Table 5 summarizes the pairing.

*Table 5. Industrial uses mapped to sensing requirements.*

| Task | Preferred depth family | First-order requirement | Usual extra sensors |
| --- | --- | --- | --- |
| Bin picking | Industrial SL / laser triangulation | Sub-mm to few-mm, high density | RGB; force/torque |
| Assembly guidance | SL or stereo at fixed standoff | Low latency, stable extrinsics | Joint encoders; IMU |
| Full-field inspection | Fringe (precise) or ToF (fast) | Repeatability, line triggering | Conveyor encoder; RGB |
| AMR 3D obstacle sense | Wide RGB-D and/or solid-state LiDAR | Field of view, frame rate, human safety | 2D safety LiDAR; IMU; wheels |

### 4.2 Autonomous mobile robots for service and logistics

Indoor service robots made RGB-D SLAM a product feature. Devices such as RealSense D400-class cameras are chosen because they balance size, power, software support, and indoor range [4,20]. Keselman et al. documented the optical and matching behaviour of the R200 and D400 families, including the fact that projector texture is an aid rather than a requirement [20]. The algorithmic backbone is well documented: RGB-D odometry, loop closure, and a metric map [19,62,63,64]. Fankhauser et al. modelled Kinect v2 specifically as a navigation sensor and showed where its systematic bias matters for terrain [45]. The remaining failures are physical. Stairs and negative obstacles (curbs, open shafts) are invisible to a waist-height two-dimensional LiDAR. A forward depth camera can reconstruct them if the near field is valid and the robot is slow enough for the integration time [45]. Outdoor last-metre robots meet sunlight and long range, which is why the same software stack often grows a LiDAR or radar [41,42].

Human-aware navigation is a semantic layer on the same geometry. Depth supplies a metric body hull; RGB pose estimators supply intent cues [15,16]. Socially acceptable clearance is then a planner parameter, not a new sensor. Active SLAM surveys discuss how a robot should move to keep that map healthy, which is a planning problem built on the same depth front-end [76].

### 4.3 UAVs and aerial robotics

On a small UAV the payload budget is measured in tens of grams and a few watts [2]. That constraint, more than any algorithm, explains why lightweight depth cameras and solid-state LiDARs appear on inspection drones while automotive-grade spinning units do not.

Obstacle avoidance is the first use. Depth gives a metric stop distance in GPS-denied corridors, forests, or plant rooms [2,79,80]. Barry, Florence, and Tedrake demonstrated tree avoidance at up to 14 m/s with a pushbroom stereo front-end running at 120 Hz on a small airframe [80]. That result is a reminder that geometric ranging, not a particular branded depth camera, is the requirement; stereo, RGB-D, and LiDAR are interchangeable only after latency, weight, and lighting are checked. Event-camera and event-stereo systems push latency into the microsecond regime for fast approach speeds [28,81,82,83]. Falanga et al. used event cameras to dodge dynamic obstacles that a frame-based pipeline would blur [81]. Miniature platforms have demonstrated onboard depth-based avoidance with tight compute envelopes [79].

Mapping and inspection is the second use. Photogrammetry from RGB already builds impressive models [84,85]. Depth or LiDAR is added when the operator needs metric scale, vegetation penetration, or a flight path that stays a fixed standoff from a girder [47,84,85]. Civil-infrastructure reviews show that the bottleneck is rarely whether a point cloud can be built. It is converting that cloud into defect locations that an engineer will trust [47].

![](figures/fig3_uav_inspection_pipeline.png)

*Figure 3. Representative UAV inspection pipeline assembled from published practice. This figure is a literature synthesis, not a system designed in the present paper.*

Figure 3 describes a representative architecture assembled from published inspection practice, not a system designed in this paper. A bridge-inspection UAV typically carries a long-range ranging sensor (solid-state LiDAR or equivalent), a high-resolution RGB camera, and an IMU [47,84,85]. Onboard software fuses range and inertia into a local metric volume and runs a lightweight network on RGB for component and surface-defect cues [47]. The aircraft uplinks an annotated model and geotagged defect hypotheses rather than raw multi-sensor video. The design is a bandwidth and trust design: inspectors re-photograph the flagged regions instead of watching hours of flight video. Multi-UAV structure-from-motion benefits from the same metric scale cue. Depth does not replace inter-vehicle communication, but it reduces the need for dense ground control [84,85].

### 4.4 Collaborative robots and human-robot interaction

Collaborative cells fail first on safety, then on programming time [3,86,87]. Depth cameras address both, with limits that must be stated.

Workspace monitoring. A ceiling or cell-side depth sensor builds a three-dimensional occupancy of the shared volume. Speed-and-separation monitoring, as framed by ISO/TS 15066, can then slow or stop the arm when a person enters a warning or protective zone [3,88]. Three-dimensional monitoring is more complete than a light curtain because it can shrink the protective volume as the arm slows and can see a person who leans over a fence. A consumer RGB-D camera is not automatically a safety-rated device. Certified implementations still need a safety controller, defined failure modes, and usually a redundant sensing channel [3,87,88]. Surveys of industrial human-robot collaboration treat safety and the user interface as the two bottlenecks that decide whether a cobot is actually used, not whether a depth demo exists [3,86]. Collision detection on the arm itself remains necessary because vision cannot see inside the contact [87].

Programming by demonstration. Tracking a tool or a marked workpiece in 3D lets a non-expert move the robot through a path [3,86]. Structured light at short range is usually sufficient. The hard parts are correspondence, occlusion by the operator, and converting a human demonstration into a collision-free, force-feasible program. Gesture and activity cues can distinguish a small set of commands or detect that a station is ready for the next part [3,16]. This is useful. It is not a substitute for a well-designed hardware enable switch.

## 5. Challenges and future perspectives

### 5.1 Persistent deployment problems

The research literature sometimes treats remaining errors as temporary. Fielded mechatronic systems suggest otherwise.

Environment and materials. NIR-based cameras saturate in sunlight [4,15]. Specular and transparent objects violate the single-bounce assumption and produce holes or biased ranges [7,35]. Coded and multi-frequency ToF can unmix some multipath, but they add capture time or hardware that a cheap module does not have [7,35]. Low-reflectance foam and black rubber starve the illuminator. Polarization, multi-frequency ToF, and radar fill-in help; none is universal. Comparative tests of ten indoor depth cameras remain the most useful reminder that material and lighting can reorder the ranking of otherwise similar devices [4].

Compute and power. Dense SLAM, TSDF fusion, and point-cloud networks are still expensive on a battery [1,21,54]. The illuminator, not only the GPU, shortens UAV endurance [2,21]. Event-based and neuromorphic pipelines are promising where the scene is sparse in time [28,81,89], but they require a different software stack.

Calibration and time. Multi-sensor extrinsics drift with temperature and shock. A one-degree boresight error is negligible for a room-scale display and unacceptable for a 50 m LiDAR-camera fusion [10,41]. Online self-calibration exists in research estimators [46,58]; it is not yet a maintenance-free commodity. Asynchronous streams and sensor dropouts can make a naively fused estimate worse than the best single sensor [42,55].

Interfaces and cost. Unlike USB webcams, depth devices still disagree on coordinate frames, distortion models, and confidence channels [4,20]. High-grade solid-state LiDAR remains expensive relative to the rest of a service robot [10]. Standardization would save more engineering time than another incremental denoiser.

*Table 6. Challenges and the honesty level of current mitigations.*

| Domain | Concrete problem | Pathway that already ships | Pathway still in research |
| --- | --- | --- | --- |
| Environment | Sunlight, glass, black parts | dToF/LiDAR, multi-echo, radar | Polarization / hyperspectral ToF |
| Compute | Dense 3D + semantics on-device | NPU for 2D nets; sparse maps | Event + spiking co-design [28,90,91] |
| Integration | Extrinsics, time, dropouts | Factory calibration; hardware sync | Lifelong self-calibration |
| Semantics | Novel clutter, moving people | Closed-set 3D detectors | 3D foundation models, Sim2Real |
| Cost / API | Proprietary frames, high unit cost | ROS drivers; a few de-facto SDKs | Safety-rated, interoperable depth |

### 5.2 Outlook

Event-based and neuromorphic sensing. Asynchronous pixels report contrast changes at microsecond latency and high dynamic range [28,89]. Combined with pulsed illumination they can support low-power depth for high-speed robots [81,82,83,92,93]. Co-design with spiking processors aims to cut the energy of spatial reasoning [90,91]. These systems will complement, not replace, frame-based RGB-D in the next product cycle.

AI near the sensor. Depth completion and a first detection head are moving into image-signal processors and sensor stacks [12,21,53]. The engineering gain is bandwidth: a robot can ship a confidence-weighted cloud or a set of objects instead of a raw 30 Hz volume. The engineering risk is silent metric failure. Safety-related channels should keep a raw or lightly filtered range path.

Richer fusion. Depth-RGB-IMU is already standard. Adding millimetre-wave radar (fog, rain, radial velocity) and thermal cameras is the practical next step, already visible in automotive datasets [42,94]. The unsolved part is a fusion integrity layer: knowing when to stop trusting a modality.

Photonics and materials. Metalenses and other flat optics can shrink camera modules [95]. Chip-scale optical phased arrays and MEMS-on-photonics LiDAR attack the scanner itself [38,39,40]. First-photon imaging and non-line-of-sight reconstructions show what is physically possible at extreme photon counts [96,97]. They are not yet bill-of-materials options for a warehouse AMR.

Infrastructure sensing. Ceiling-mounted depth in factories and intelligent spaces can offload onboard mapping. The idea is sound. The obstacles are privacy, networking, and a shared metric frame that every vendor agrees to.

## 6. Conclusion

Depth vision in mechatronics did not evolve as a single replacement chain. Structured light made dense, inexpensive, close-range geometry ordinary. ToF made that geometry small enough for mobile heads and phones. Solid-state LiDAR made long-range ranging compatible with vibration-sensitive platforms. Algorithms (completion, tight-coupled odometry, RGB-D SLAM, and 3D semantics) converted those measurements into poses, maps, grasps, and safety zones.

The remaining limits are mostly physical and organizational: sunlight and materials, watts and memory, calibration, and fragmented interfaces. A next-generation system is unlikely to be one perfect depth camera. It is more likely to be a small set of complementary ranges, an estimator that knows its integrity, and, where possible, a shared map that the machine does not have to rebuild on every shift.

For practitioners, the operational conclusion is conservative. Choose the sensor by operating envelope, not by marketing generation. Budget calibration and lighting as first-class design items. Keep a metric, low-level range channel whenever the output can stop a motor.

## Author contributions

Bo Zhang drafted the review, organized the literature, and prepared the comparative tables and figures. Hongchao Cui conceived the hardware-centered scope, revised the manuscript, and supervised the work. Both authors approved the final version.

## Conflicts of interest

The authors declare no conflict of interest.

## Data availability

No new datasets were generated. All cited sources are listed in the References.

## References

[1] Cadena C, Carlone L, Carrillo H, Latif Y, Scaramuzza D, Neira J, Reid I, Leonard JJ. Past, present, and future of simultaneous localization and mapping: Toward the robust-perception age. IEEE Transactions on Robotics. 2016;32(6):1309-1332. doi:10.1109/TRO.2016.2624754

[2] Floreano D, Wood RJ. Science, technology and the future of small autonomous drones. Nature. 2015;521:460-466. doi:10.1038/nature14542

[3] Villani V, Pini F, Leali F, Secchi C. Survey on human-robot collaboration in industrial settings: Safety, intuitive interfaces and applications. Mechatronics. 2018;55:248-266. doi:10.1016/j.mechatronics.2018.02.009

[4] Halmetschlager-Funek G, Suchi M, Kampel M, Vincze M. An empirical evaluation of ten depth cameras: Bias, precision, lateral noise, different lighting conditions and materials, and multiple sensor setups in indoor environments. IEEE Robotics and Automation Magazine. 2019;26(1):67-77. doi:10.1109/MRA.2018.2852795

[5] Zhang S. High-speed 3D shape measurement with structured light methods: A review. Optics and Lasers in Engineering. 2012;50(8):1067-1074. doi:10.1016/j.optlaseng.2012.03.004

[6] Geng J. Structured-light 3D surface imaging: a tutorial. Advances in Optics and Photonics. 2011;3(2):128-160. doi:10.1364/AOP.3.000128

[7] Foix S, Alenya G, Torras C. Lock-in time-of-flight (ToF) cameras: A survey. IEEE Sensors Journal. 2011;11(9):1917-1926. doi:10.1109/JSEN.2010.2101060

[8] Horaud R, Hansard M, Evangelidis G, Menier C. An overview of depth cameras and range scanners based on time-of-flight technologies. Machine Vision and Applications. 2016;27(7):1005-1020. doi:10.1007/s00138-016-0784-4

[9] Ho CP, Li N, Xue J, Lim LW, Chen G, Fu YH, Lee LYT. A progress review on solid-state LiDAR and nanophotonics-based LiDAR sensors. Laser & Photonics Reviews. 2022;16(11):2100511. doi:10.1002/lpor.202100511

[10] Roriz R, Cabral J, Gomes T. Automotive LiDAR technology: A survey. IEEE Transactions on Intelligent Transportation Systems. 2022;23(7):6282-6297. doi:10.1109/TITS.2021.3086804

[11] Scharstein D, Szeliski R. A taxonomy and evaluation of dense two-frame stereo correspondence algorithms. International Journal of Computer Vision. 2002;47(1-3):7-42. doi:10.1023/A:1014573219977

[12] Eigen D, Puhrsch C, Fergus R. Depth map prediction from a single image using a multi-scale deep network. In: Advances in Neural Information Processing Systems 27; 2014. p. 2366-2374.

[13] Godard C, Mac Aodha O, Brostow GJ. Unsupervised monocular depth estimation with left-right consistency. In: Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR); 2017. p. 270-279. doi:10.1109/CVPR.2017.699

[14] Khoshelham K, Elberink SO. Accuracy and resolution of Kinect depth data for indoor mapping applications. Sensors. 2012;12(2):1437-1454. doi:10.3390/s120201437

[15] Sarbolandi H, Lefloch D, Kolb A. Kinect range sensing: Structured-light versus Time-of-Flight Kinect. Computer Vision and Image Understanding. 2015;139:1-20. doi:10.1016/j.cviu.2015.05.006

[16] Shotton J, Fitzgibbon A, Cook M, Sharp T, Finocchio M, Moore R, Kipman A, Blake A. Real-time human pose recognition in parts from single depth images. In: Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR); 2011. p. 1297-1304. doi:10.1109/CVPR.2011.5995316

[17] Newcombe RA, Izadi S, Hilliges O, Molyneaux D, Kim D, Davison AJ, Kohli P, Shotton J, Hodges S, Fitzgibbon A. KinectFusion: Real-time dense surface mapping and tracking. In: Proceedings of the 10th IEEE International Symposium on Mixed and Augmented Reality (ISMAR); 2011. p. 127-136. doi:10.1109/ISMAR.2011.6092378

[18] Izadi S, Kim D, Hilliges O, Molyneaux D, Newcombe R, Kohli P, Shotton J, Hodges S, Freeman D, Davison A, Fitzgibbon A. KinectFusion: Real-time 3D reconstruction and interaction using a moving depth camera. In: Proceedings of the 24th Annual ACM Symposium on User Interface Software and Technology (UIST); 2011. p. 559-568. doi:10.1145/2047196.2047270

[19] Henry P, Krainin M, Herbst E, Ren X, Fox D. RGB-D mapping: Using Kinect-style depth cameras for dense 3D modeling of indoor environments. The International Journal of Robotics Research. 2012;31(5):647-663. doi:10.1177/0278364911434148

[20] Keselman L, Woodfill JI, Grunnet-Jepsen A, Bhowmik A. Intel RealSense stereoscopic depth cameras. In: IEEE Conference on Computer Vision and Pattern Recognition Workshops (CVPRW); 2017. p. 1267-1276. doi:10.1109/CVPRW.2017.167

[21] Gyongy I, Dutton NAW, Henderson RK. Direct time-of-flight single-photon imaging. IEEE Transactions on Electron Devices. 2022;69(6):2794-2805. doi:10.1109/TED.2021.3131430

[22] Kolb A, Barth E, Koch R, Larsen R. Time-of-flight cameras in computer graphics. Computer Graphics Forum. 2010;29(1):141-159. doi:10.1111/j.1467-8659.2009.01583.x

[23] Zanuttigh P, Marin G, Dal Mutto C, Dominio F, Minto L, Cortelazzo GM. Time-of-Flight and Structured Light Depth Cameras: Technology and Applications. Cham: Springer; 2016. doi:10.1007/978-3-319-30973-6

[24] Giancola S, Valenti M, Sala R. A Survey on 3D Cameras: Metrological Comparison of Time-of-Flight, Structured-Light and Active Stereoscopy Technologies. Cham: Springer; 2018. doi:10.1007/978-3-319-91761-0

[25] Taketomi T, Uchiyama H, Ikeda S. Visual SLAM algorithms: A survey from 2010 to 2016. IPSJ Transactions on Computer Vision and Applications. 2017;9:16. doi:10.1186/s41074-017-0027-2

[26] Macario Barros A, Michel M, Moline Y, Corre G, Carrel F. A comprehensive survey of visual SLAM algorithms. Robotics. 2022;11(1):24. doi:10.3390/robotics11010024

[27] Wang Y, Tian Y, Chen J, Xu K, Ding X. A survey of visual SLAM in dynamic environment: The evolution from geometric to semantic approaches. IEEE Transactions on Instrumentation and Measurement. 2024;73:1-21. doi:10.1109/TIM.2024.3379090

[28] Gallego G, Delbruck T, Orchard G, Bartolozzi C, Taba B, Censi A, Leutenegger S, Davison AJ, Conradt J, Daniilidis K, Scaramuzza D. Event-based vision: A survey. IEEE Transactions on Pattern Analysis and Machine Intelligence. 2022;44(1):154-180. doi:10.1109/TPAMI.2020.3008413

[29] Li Y, Ibanez-Guzman J. Lidar for autonomous driving: The principles, challenges, and trends for automotive lidar and perception systems. IEEE Signal Processing Magazine. 2020;37(4):50-61. doi:10.1109/MSP.2020.2973615

[30] Raj T, Hashim FH, Huddin AB, Ibrahim MF, Hussain A. A survey on LiDAR scanning mechanisms. Electronics. 2020;9(5):741. doi:10.3390/electronics9050741

[31] Lange R, Seitz P. Solid-state time-of-flight range camera. IEEE Journal of Quantum Electronics. 2001;37(3):390-397. doi:10.1109/3.910448

[32] Niclass C, Soga M, Kato S, Matsubara H, Kagami M. A 0.18-um CMOS SoC for a 100-m-range 10-frame/s 200 x 96-pixel time-of-flight depth sensor. IEEE Journal of Solid-State Circuits. 2013;48(2):559-572. doi:10.1109/JSSC.2012.2227607

[33] Lachat E, Macher H, Landes T, Grussenmeyer P. Assessment and calibration of a RGB-D camera (Kinect v2 sensor) towards a potential use for close-range 3D modeling. Remote Sensing. 2015;7(10):13070-13097. doi:10.3390/rs71013070

[34] Pagliari D, Pinto L. Calibration of Kinect for Xbox One and comparison between the two generations of Microsoft sensors. Sensors. 2015;15(11):27569-27589. doi:10.3390/s151127569

[35] Kadambi A, Whyte R, Bhandari A, Streeter L, Barsi C, Dorrington A, Raskar R. Coded time of flight cameras: sparse deconvolution to address multipath interference and recover time profiles. ACM Transactions on Graphics. 2013;32(6):167. doi:10.1145/2508363.2508428

[36] Kim I, Martins RJ, Jang J, Badloe T, Khadir S, Jung HY, Kim H, Kim J, Genevet P, Rho J. Nanophotonics for light detection and ranging technology. Nature Nanotechnology. 2021;16:508-524. doi:10.1038/s41565-021-00895-3

[37] Park J, Jeong BG, Kim SI, Lee D, Kim J, Shin C, Lee CB, Otsuka T, Kyoung J, Kim S, Yang KY, Park YY, Lee J, Hwang I, Jang J, Song SH, Brongersma ML, Ha K, Hwang SW, Choo H, Choi BL. All-solid-state spatial light modulator with independent phase and amplitude control for three-dimensional LiDAR applications. Nature Nanotechnology. 2021;16:69-76. doi:10.1038/s41565-020-00787-y

[38] Sun J, Timurdogan E, Yaacobi A, Hosseini ES, Watts MR. Large-scale nanophotonic phased array. Nature. 2013;493:195-199. doi:10.1038/nature11727

[39] Poulton CV, Yaacobi A, Cole DB, Byrd MJ, Raval M, Vermeulen D, Watts MR. Coherent solid-state LIDAR with silicon photonic optical phased arrays. Optics Letters. 2017;42(20):4091-4094. doi:10.1364/OL.42.004091

[40] Zhang X, Kwon K, Henriksson J, Luo J, Wu MC. A large-scale microelectromechanical-systems-based silicon photonic LiDAR. Nature. 2022;603:253-258. doi:10.1038/s41586-022-04415-8

[41] Debeunne C, Vivet D. A review of visual-LiDAR fusion based simultaneous localization and mapping. Sensors. 2020;20(7):2068. doi:10.3390/s20072068

[42] Yeong DJ, Velasco-Hernandez G, Barry J, Walsh J. Sensor and sensor fusion technology in autonomous vehicles: A review. Sensors. 2021;21(6):2140. doi:10.3390/s21062140

[43] Correll N, Bekris KE, Berenson D, Brock O, Causo A, Hauser K, Okada K, Rodriguez A, Romano JM, Wurman PR. Analysis and observations from the first Amazon Picking Challenge. IEEE Transactions on Automation Science and Engineering. 2018;15(1):172-188. doi:10.1109/TASE.2016.2600527

[44] ten Pas A, Gualtieri M, Saenko K, Platt R. Grasp pose detection in point clouds. The International Journal of Robotics Research. 2017;36(13-14):1455-1473. doi:10.1177/0278364917735594

[45] Fankhauser P, Bloesch M, Rodriguez D, Kaestner R, Hutter M, Siegwart R. Kinect v2 for mobile robot navigation: Evaluation and modeling. In: International Conference on Advanced Robotics (ICAR); 2015. p. 388-394. doi:10.1109/ICAR.2015.7251485

[46] Campos C, Elvira R, Rodriguez JJG, Montiel JMM, Tardos JD. ORB-SLAM3: An accurate open-source library for visual, visual-inertial, and multimap SLAM. IEEE Transactions on Robotics. 2021;37(6):1874-1890. doi:10.1109/TRO.2021.3075644

[47] Spencer BF Jr, Hoskere V, Narazaki Y. Advances in computer vision-based civil infrastructure inspection and monitoring. Engineering. 2019;5(2):199-222. doi:10.1016/j.eng.2018.11.030

[48] Kopf J, Cohen MF, Lischinski D, Uyttendaele M. Joint bilateral upsampling. ACM Transactions on Graphics. 2007;26(3):96. doi:10.1145/1276377.1276497

[49] Silberman N, Hoiem D, Kohli P, Fergus R. Indoor segmentation and support inference from RGBD images. In: Computer Vision - ECCV 2012. Springer; 2012. p. 746-760. doi:10.1007/978-3-642-33715-4_54

[50] Laina I, Rupprecht C, Belagiannis V, Tombari F, Navab N. Deeper depth prediction with fully convolutional residual networks. In: International Conference on 3D Vision (3DV); 2016. p. 239-248. doi:10.1109/3DV.2016.32

[51] Godard C, Mac Aodha O, Firman M, Brostow GJ. Digging into self-supervised monocular depth estimation. In: Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV); 2019. p. 3828-3838. doi:10.1109/ICCV.2019.00393

[52] Uhrig J, Schneider N, Schneider L, Franke U, Brox T, Geiger A. Sparsity invariant CNNs. In: International Conference on 3D Vision (3DV); 2017. p. 11-20. doi:10.1109/3DV.2017.00012

[53] Ma F, Karaman S. Sparse-to-dense: Depth prediction from sparse depth samples and a single image. In: IEEE International Conference on Robotics and Automation (ICRA); 2018. p. 4796-4803. doi:10.1109/ICRA.2018.8460184

[54] Guo Y, Wang H, Hu Q, Liu H, Liu L, Bennamoun M. Deep learning for 3D point clouds: A survey. IEEE Transactions on Pattern Analysis and Machine Intelligence. 2021;43(12):4338-4364. doi:10.1109/TPAMI.2020.3005434

[55] Thrun S, Burgard W, Fox D. Probabilistic Robotics. Cambridge, MA: MIT Press; 2005.

[56] Leutenegger S, Lynen S, Bosse M, Siegwart R, Furgale P. Keyframe-based visual-inertial odometry using nonlinear optimization. The International Journal of Robotics Research. 2015;34(3):314-334. doi:10.1177/0278364914554813

[57] Forster C, Carlone L, Dellaert F, Scaramuzza D. On-manifold preintegration for real-time visual-inertial odometry. IEEE Transactions on Robotics. 2017;33(1):1-21. doi:10.1109/TRO.2016.2597321

[58] Qin T, Li P, Shen S. VINS-Mono: A robust and versatile monocular visual-inertial state estimator. IEEE Transactions on Robotics. 2018;34(4):1004-1020. doi:10.1109/TRO.2018.2853729

[59] Bloesch M, Omari S, Hutter M, Siegwart R. Robust visual inertial odometry using a direct EKF-based approach. In: IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS); 2015. p. 298-304. doi:10.1109/IROS.2015.7353389

[60] Whelan T, Leutenegger S, Salas-Moreno RF, Glocker B, Davison AJ. ElasticFusion: Dense SLAM without a pose graph. In: Robotics: Science and Systems; 2015. doi:10.15607/RSS.2015.XI.001

[61] Dai A, Niessner M, Zollhofer M, Izadi S, Theobalt C. BundleFusion: Real-time globally consistent 3D reconstruction using on-the-fly surface reintegration. ACM Transactions on Graphics. 2017;36(4):76a. doi:10.1145/3072959.3073615

[62] Endres F, Hess J, Sturm J, Cremers D, Burgard W. 3-D mapping with an RGB-D camera. IEEE Transactions on Robotics. 2014;30(1):177-187. doi:10.1109/TRO.2013.2279412

[63] Sturm J, Engelhard N, Endres F, Burgard W, Cremers D. A benchmark for the evaluation of RGB-D SLAM systems. In: IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS); 2012. p. 573-580. doi:10.1109/IROS.2012.6385773

[64] Mur-Artal R, Tardos JD. ORB-SLAM2: An open-source SLAM system for monocular, stereo, and RGB-D cameras. IEEE Transactions on Robotics. 2017;33(5):1255-1262. doi:10.1109/TRO.2017.2705103

[65] Rosinol A, Abate M, Chang Y, Carlone L. Kimera: an open-source library for real-time metric-semantic localization and mapping. In: IEEE International Conference on Robotics and Automation (ICRA); 2020. p. 1689-1696. doi:10.1109/ICRA40945.2020.9196885

[66] Tian Y, Chang Y, Herrera Arias F, Nieto-Granda C, How JP, Carlone L. Kimera-Multi: Robust, distributed, dense metric-semantic SLAM for multi-robot systems. IEEE Transactions on Robotics. 2022;38(4):2022-2038. doi:10.1109/TRO.2021.3137751

[67] Engel J, Schops T, Cremers D. LSD-SLAM: Large-scale direct monocular SLAM. In: Computer Vision - ECCV 2014. Springer; 2014. p. 834-849. doi:10.1007/978-3-319-10605-2_54

[68] Rusu RB, Cousins S. 3D is here: Point Cloud Library (PCL). In: IEEE International Conference on Robotics and Automation (ICRA); 2011. p. 1-4. doi:10.1109/ICRA.2011.5980567

[69] Besl PJ, McKay ND. A method for registration of 3-D shapes. IEEE Transactions on Pattern Analysis and Machine Intelligence. 1992;14(2):239-256. doi:10.1109/34.121791

[70] Hornung A, Wurm KM, Bennewitz M, Stachniss C, Burgard W. OctoMap: An efficient probabilistic 3D mapping framework based on octrees. Autonomous Robots. 2013;34:189-206. doi:10.1007/s10514-012-9321-0

[71] Oleynikova H, Taylor Z, Fehr M, Siegwart R, Nieto J. Voxblox: Incremental 3D Euclidean signed distance fields for on-board MAV planning. In: IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS); 2017. p. 1366-1373. doi:10.1109/IROS.2017.8202315

[72] Qi CR, Su H, Mo K, Guibas LJ. PointNet: Deep learning on point sets for 3D classification and segmentation. In: Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR); 2017. p. 652-660. doi:10.1109/CVPR.2017.16

[73] Qi CR, Yi L, Su H, Guibas LJ. PointNet++: Deep hierarchical feature learning on point sets in a metric space. In: Advances in Neural Information Processing Systems 30; 2017.

[74] Hodan T, Michel F, Brachmann E, Kehl W, Glent Buch A, Kraft D, Drost B, Vidal J, Ihrke S, Zabulis X, Sahin C, Manhardt F, Tombari F, Kim TK, Matas J, Rother C. BOP: Benchmark for 6D object pose estimation. In: Computer Vision - ECCV 2018. Springer; 2018. p. 19-34. doi:10.1007/978-3-030-01249-6_2

[75] Xiang Y, Schmidt T, Narayanan V, Fox D. PoseCNN: A convolutional neural network for 6D object pose estimation in cluttered scenes. In: Robotics: Science and Systems; 2018. doi:10.15607/RSS.2018.XIV.019

[76] Placed JA, Strader J, Carrillo H, Atanasov N, Indelman V, Carlone L, Castellanos JA. A survey on active simultaneous localization and mapping: State of the art and new frontiers. IEEE Transactions on Robotics. 2023;39(3):1686-1705. doi:10.1109/TRO.2023.3248510

[77] Mahler J, Liang J, Niyaz S, Laskey M, Doan R, Liu X, Ojea JA, Goldberg K. Dex-Net 2.0: Deep learning to plan robust grasps with synthetic point clouds and analytic grasp metrics. In: Robotics: Science and Systems; 2017. doi:10.15607/RSS.2017.XIII.058

[78] Zeng A, Yu KT, Song S, Suo D, Walker E, Rodriguez A, Xiao J. Multi-view self-supervised deep learning for 6D pose estimation in the Amazon Picking Challenge. In: IEEE International Conference on Robotics and Automation (ICRA); 2017. p. 1386-1393. doi:10.1109/ICRA.2017.7989165

[79] Muller H, Niculescu V, Polonelli T, Magno M, Benini L. Robust and efficient depth-based obstacle avoidance for autonomous miniaturized UAVs. IEEE Transactions on Robotics. 2023;39(6):4935-4951. doi:10.1109/TRO.2023.3325812

[80] Barry AJ, Florence PR, Tedrake R. High-speed autonomous obstacle avoidance with pushbroom stereo. Journal of Field Robotics. 2018;35(1):52-68. doi:10.1002/rob.21741

[81] Falanga D, Kleber K, Scaramuzza D. Dynamic obstacle avoidance for quadrotors with event cameras. Science Robotics. 2020;5(40):eaaz9712. doi:10.1126/scirobotics.aaz9712

[82] Zhou Y, Gallego G, Shen S. Event-based stereo visual odometry. IEEE Transactions on Robotics. 2021;37(5):1433-1450. doi:10.1109/TRO.2021.3062252

[83] He B, Wang Z, Zhou Y, Chen J, Singh CD, Li H, Gao Y, Shen S, Wang K, Cao Y, Xu C, Aloimonos Y, Gao F, Fermuller C. Microsaccade-inspired event camera for robotics. Science Robotics. 2024;9(90):eadj8124. doi:10.1126/scirobotics.adj8124

[84] Nex F, Remondino F. UAV for 3D mapping applications: a review. Applied Geomatics. 2014;6:1-15. doi:10.1007/s12518-013-0120-x

[85] Colomina I, Molina P. Unmanned aerial systems for photogrammetry and remote sensing: A review. ISPRS Journal of Photogrammetry and Remote Sensing. 2014;92:79-97. doi:10.1016/j.isprsjprs.2014.02.013

[86] Ajoudani A, Zanchettin AM, Ivaldi S, Albu-Schaffer A, Kosuge K, Khatib O. Progress and prospects of the human-robot collaboration. Autonomous Robots. 2018;42:957-975. doi:10.1007/s10514-017-9677-2

[87] Haddadin S, De Luca A, Albu-Schaffer A. Robot collisions: A survey on detection, isolation, and identification. IEEE Transactions on Robotics. 2017;33(6):1292-1312. doi:10.1109/TRO.2017.2725543

[88] International Organization for Standardization. ISO/TS 15066:2016. Robots and robotic devices - Collaborative robots. Geneva: ISO; 2016.

[89] Lichtsteiner P, Posch C, Delbruck T. A 128 x 128 120 dB 15 us latency asynchronous temporal contrast vision sensor. IEEE Journal of Solid-State Circuits. 2008;43(2):566-576. doi:10.1109/JSSC.2007.914337

[90] Roy K, Jaiswal A, Panda P. Towards spike-based machine intelligence with neuromorphic computing. Nature. 2019;575:607-617. doi:10.1038/s41586-019-1677-2

[91] Davies M, Srinivasa N, Lin TH, Chinya G, Cao Y, Choday SH, Dimou G, Joshi P, Imam N, Jain S, Liao Y, Lin CK, Lines A, Liu R, Mathaikutty D, McCoy S, Paul A, Tse J, Venkataramanan G, Weng YH, Wild A, Yang Y, Wang H. Loihi: A neuromorphic manycore processor with on-chip learning. IEEE Micro. 2018;38(1):82-99. doi:10.1109/MM.2018.112130359

[92] Rebecq H, Horstschaefer T, Gallego G, Scaramuzza D. EVO: A geometric approach to event-based 6-DOF parallel tracking and mapping in real time. IEEE Robotics and Automation Letters. 2017;2(2):593-600. doi:10.1109/LRA.2016.2645143

[93] Guo S, Gallego G. CMax-SLAM: Event-based rotational-motion bundle adjustment and SLAM system using contrast maximization. IEEE Transactions on Robotics. 2024;40:2442-2461. doi:10.1109/TRO.2024.3378443

[94] Caesar H, Bankiti V, Lang AH, Vora S, Liong VE, Xu Q, Krishnan A, Pan Y, Baldan G, Beijbom O. nuScenes: A multimodal dataset for autonomous driving. In: Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR); 2020. p. 11621-11631. doi:10.1109/CVPR42600.2020.01164

[95] Khorasaninejad M, Capasso F. Metalenses: Versatile multifunctional photonic components. Science. 2017;358(6367):eaam8100. doi:10.1126/science.aam8100

[96] Kirmani A, Venkatraman D, Shin D, Colaco A, Wong FNC, Shapiro JH, Goyal VK. First-photon imaging. Science. 2014;343(6166):58-61. doi:10.1126/science.1246775

[97] O'Toole M, Lindell DB, Wetzstein G. Confocal non-line-of-sight imaging based on the light-cone transform. Nature. 2018;555:338-341. doi:10.1038/nature25489
