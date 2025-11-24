import pygame
from pygame.locals import *
from classes import Player, Object, Station, Resource

pygame.init()

SCREEN_WIDTH = 1080
WORLD_WIDTH = 5200
SCREEN_HEIGHT = 720

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
ATTRIBUTES = {"containment_vault":{"volatile":["instability",
                                                "reaction_time", 
                                                "safe_distance",
                                                "containment_pressure"
                                                ],
                                    "hazardous":["toxicity",
                                                "corrosiveness",
                                                "biohazard_rating",
                                                "odor_strength"],
                                    "sentient":["awareness_level",
                                                "communication_style",
                                                "response_latency",
                                                "mood_index",
                                                "cognitive_mass"],
                                    "parasitic":["host_type",
                                                "drain_rate",
                                                "reproduction_time",
                                                "nutrient_requirements"],
                                    "temporal_distortion":["time_dilation",
                                                            "loop_duration",
                                                            "chronological_offset",
                                                            "echo_mass"],
                                    "gravitational_anomaly":["microgravity_field",
                                                            "presumed_density",
                                                            "pull_strength",
                                                            "spatial_warp_degree"]
                                    },
            "documentation_cubicle":{"bureaucratic":["redundancy_index",
                                                    "approval_delay",
                                                    "stamp_count",
                                                    "filing_temperature"],
                                    "linguistic":["language_complexity",
                                                "language_origin",
                                                "speaker_number",
                                                "readability"],
                                    "archival":["age",
                                                "catalog_number",
                                                "fragility",
                                                "preservation_priority"],
                                    "mnemonic":["recall_difficulty",
                                                "emotional_load",
                                                "memory_resonance",
                                                "cognitive_load"],
                                    "prophetic":["accuracy_rate",
                                                "timeline_divergence",
                                                "prediction_window",
                                                "message_clarity",
                                                ],
                                    "instructional":["instructional_clarity",
                                                    "compliance_rate",
                                                    "warning_level",
                                                    "user_steps",
                                                    "diagram_quality"
                                                    ]
                                    },
            "recycler":{"metallic":["element_purity",
                                    "conductivity",
                                    "melting_point",
                                    "tensile_strength"
                                    ],
                        "organic":["humidity",
                                    "biomass",
                                    "pH",
                                    "state_of_decomposition"
                                    ],
                        "synthetic":["polymer_type",
                                    "rigidity",
                                    "thermal_resistance",
                                    "color_index"],
                        "biodegradable":["breakdown_time",
                                        "microbial_affinity",
                                        "compost_value",
                                        "moisture_content"],
                        "recyclable":["energy_yield",
                                    "refraction_index",
                                    "crystallinity",
                                    ]
                        },
            "dimensional_export_tube":{"phase_fluid":["viscosity",
                                                    "transparency",
                                                    "shift_rate",
                                                    "interphase_temperature",
                                                    "phases"
                                                    ],
                                    "extradimensional":["dimension_origin",
                                                        "anchor_mass",
                                                        "arrival_form",
                                                        "quantum_lag",
                                                        "origin_layer"
                                                        ],
                                    "nonlocal":["coordinates",
                                                "displacement_interval",
                                                "tether_length",
                                                "locality_score"
                                                ],
                                    "spectral":["luminosity",
                                                "opacity",
                                                "flicker_rate",
                                                "hue_instability"],
                                    "dreamlike":["loss_of_self",
                                                "logic_strength",
                                                "imagery_strength",
                                                "lucidity"],
                                    },
            "lost_and_found":{"misplaced":["owner_id",
                                            "last_known_location",
                                            "dust_level",
                                            "retrieval_probability"],
                                "mundane":["weight",
                                            "wear_level",
                                            "usefulness",
                                            "expiry_date"],
                                "personal":["sentimental_value",
                                            "pocket_fit",
                                            "perfume_strength",
                                            "usage_frequency"],
                                "damaged":["crack_length",
                                            "repairability",
                                            "rust_index",
                                            "remaining_functionality"],
                                "unidentified":["entry_timestamp",
                                                "preliminary_value",
                                                "detection_confidence",
                                                "mystery_index"],
                                "nostalgic":["memory_strength",
                                            "era",
                                            "resonance"]
                                }
            }

OBJECT_TIMES = {1:1800, 2:1500, 3:1800, 4:2700, 5:2700}

clock = pygame.time.Clock()

player = Player("PlayerSideStillScaled.png", 90, 540, 5)
background_image = pygame.image.load("working_bg.png").convert()
world_stability = Resource("world_stability", 100, 0)
sanity = Resource("sanity", 100, 230)
time_distortion = Resource("time_distortion", 100, 370)
resources = [world_stability, sanity, time_distortion]

objects_one = [
    Object(
        "A Coffee Mug that Pours Upside-Down",
        "A coffee mug that defies gravity...",
        "ScaledCoffee.png",
        3,
        ["synthetic", "biodegradable", "gravititational_anomaly"],
        analysis_data = {
            "polymer_type": "Inverted-ceramic blend",
            "moisture_content": "...Really high.",
            "microgravity_field": "For some reason, only liquids inside the cup are affected."
        },
    ),
    Object(
        "An Equation Leaking Color",
        "This derivative truly embraced the rainbow.",
        "Equation_Scaled.png",
        5,
        ["bureaucratic", "linguistic", "spectral"],
        analysis_data={
            "hue_instability": "Appears to change color every time you look at it. You can't name the colors. You shouldn't try.",
            "redundancy_index": "Infinity if you're not in STEM.",
            "speaker_number": "Everyone in Calculus and Vectors - unfortunately."
        }
    )
]

analyzer = Station("Analyzer.png", 900, 700, "analyzer")
conveyor = Station("conveyor.png", 0, 720, "conveyor")
conveyor_origin = Station("Conveyor_origin.png", 0, 680, "conveyor_origin")

objects = pygame.sprite.Group()

stations = pygame.sprite.Group()
stations.add(analyzer)
stations.add(conveyor)


decorations = pygame.sprite.Group()

analyzer_rends, analyzer_rects = [], []
font = pygame.font.Font('freesansbold.ttf', 22)
level = 1
frame = 0
objectNum = 0
newObject = False
running = True
while running:
    for event in pygame.event.get(): 
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

    pressed_keys = pygame.key.get_pressed()
    player.update_pos(pressed_keys)
    if level == 1:
        if frame % OBJECT_TIMES[level] == 0 and not newObject:
            if objectNum < len(objects_one):
                objects.add(objects_one[objectNum])
                objectNum += 1
        for object in objects:
            object.update(frame)
            if object.state == "analysis":
                crash = False
                for other_obj in objects:
                    if other_obj.state == "analysis_complete":
                        crash = True
                        if "volatile" in other_obj.tags + object.tags or "hazardous" in other_obj.tags + object.tags:
                            world_stability.update(world_stability.current_amount - 10)
                        else:
                            sanity.update(sanity.current_amount - 5)
                        object.state = "crashed"
                if not crash:
                    analyzer_pop_up, analyzer_rends, analyzer_rects = analyzer.analyze_object(object)
                    decorations.add(analyzer_pop_up)
                    object.state = "analysis_complete"
            

    # --- CAMERA LOGIC ---
    camera_x = player.rect.x - SCREEN_WIDTH // 2
    camera_x = max(0, min(camera_x, WORLD_WIDTH - SCREEN_WIDTH))

    # --- DRAW ---
    screen.blit(background_image, (-camera_x, 0))

    for station in stations:
        screen.blit(station.image, (station.rect.x - camera_x, station.rect.y))

    for sprite in objects:
        screen.blit(sprite.image, (sprite.rect.x - camera_x, sprite.rect.y))
    
    screen.blit(conveyor_origin.image, (conveyor_origin.rect.x - camera_x, conveyor_origin.rect.y))
    
    for sprite in decorations:
        sprite.animate(frame)
        screen.blit(sprite.image, (sprite.rect.x - camera_x, sprite.rect.y))
    
    if analyzer_rects:
        for rend, rect in zip(analyzer_rends, analyzer_rects):
            if frame % analyzer_pop_up.spd == 0:
                rect.y += analyzer_pop_up.dir
            screen.blit(rend, (rect.x - camera_x, rect.y))
    
    for resource in resources:
        rend, rect = resource.display(font)
        screen.blit(rend, (rect.x, rect.y))
    
    screen.blit(player.image, (player.rect.x - camera_x, player.rect.y))

    pygame.display.update()
    frame += 1
    clock.tick(60)

pygame.quit()
