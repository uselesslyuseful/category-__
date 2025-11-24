import pygame
from pygame.locals import *
from collections import Counter

WORLD_WIDTH = 5200
SCREEN_HEIGHT = 720

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

class Object(pygame.sprite.Sprite):
    def __init__(self, name, desc, image, spd, tags, analysis_data, station_num = 1, value = 1):
        super().__init__()
        self.name = name
        self.desc = desc
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect(bottomleft = (0, 550))
        self.spd = spd
        self.state = "onConveyor"
        self.tags = tags
        self.analysis_data = analysis_data
        self.value = value
        self.station_num = station_num
        self.station = self.correct_destination(self.analysis_data, ATTRIBUTES, self.station_num)
    def update(self, frame):
        if self.state == "onConveyor":
            if frame % 2 == 0:
                self.rect.x += self.spd
        if self.rect.centerx >= 1100 and self.state == "onConveyor":
            self.state = "analysis"
    @staticmethod
    def correct_destination(analysis_data, ATTRIBUTES, station_num):
        factor_list = []
        station_list = []
        for factor in analysis_data:
            for station, properties in ATTRIBUTES.items():
                for property in properties:
                    if factor in properties[property]:
                        factor_list.append(station)
        station_counts = Counter(factor_list)
        for i in range(station_num):
            station_list.append(station_counts[list(station_counts.keys())[i]])
        return station_list

        

class Decoration(pygame.sprite.Sprite):
    def __init__(self, image, x_pos, y_pos, spd, lim):
        super().__init__()
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect(center=(x_pos, y_pos))
        self.ogy_pos = y_pos
        self.spd = spd
        self.lim = lim
        self.dir = 1
    def animate(self, frame):
        if frame % self.spd == 0:
            self.rect.y += self.dir
            if abs(self.rect.y - self.ogy_pos) >= self.lim:
                # clamp to limit to avoid overshoot
                if self.dir == 1:
                    self.rect.y = self.ogy_pos + self.lim
                else:
                    self.rect.y = self.ogy_pos - self.lim
                self.dir *= -1

        

class Player(pygame.sprite.Sprite):
    def __init__(self, image, x_pos, y_pos, spd):
        super().__init__()
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect(center=(x_pos, y_pos))
        self.spd = spd
    
    def update_pos(self, pressed_keys):
        if pressed_keys[K_LEFT]:
            self.rect.x -= self.spd
        if pressed_keys[K_RIGHT]:
            self.rect.x += self.spd
        
        # clamp within WORLD width
        self.rect.x = max(0, min(self.rect.x, WORLD_WIDTH - self.rect.width))

class Station(pygame.sprite.Sprite):
    def __init__(self, image, x_pos, y_pos, type):
        super().__init__()
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect(bottomleft = (x_pos, y_pos))
        self.type = type
    def analyze_object(self, obj):
        analyzer_popup = Decoration("Analyzer_Popup.png", self.rect.centerx - 15, self.rect.centery - 430, 2, 20)
        title_font = pygame.font.Font('freesansbold.ttf', 18)
        font = pygame.font.Font('freesansbold.ttf', 15)

        # Wrap BOTH title and description
        title_lines = Station.render_text_wrapped(obj.name, title_font, (255,255,255), 400)
        desc_lines  = Station.render_text_wrapped(obj.desc,  font, (255,255,255), 400)
        analysis_lines = []
        analysis_rends = []
        for key, value in obj.analysis_data.items():
            line = f"{key.capitalize()}: {value}"
            analysis_lines.append(line)
        for line in analysis_lines:
            analysis_rends += Station.render_text_wrapped(line,  font, (255,255,255), 400)
        
        analyzer_rends = title_lines + desc_lines + analysis_rends

        # Build rects with spacing
        analyzer_rects = []

        line_spacing = 19
        total_lines = len(analyzer_rends)
        total_height = total_lines * line_spacing

        # Center the entire block around analyzer_popup.rect.centery
        start_y = analyzer_popup.rect.centery - (total_height // 2) + 150

        for i, rend in enumerate(analyzer_rends):
            rect = rend.get_rect(center=(
                analyzer_popup.rect.centerx,
                start_y + i * line_spacing
            ))
            analyzer_rects.append(rect)

        return analyzer_popup, analyzer_rends, analyzer_rects

    @staticmethod
    def render_text_wrapped(text, font, color, max_width):
        words = text.split(" ")
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            test_surface = font.render(test_line, True, color)

            if test_surface.get_width() <= max_width:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word + " "

        if current_line:
            lines.append(current_line.strip())

        # Turn lines into Surfaces
        rendered_lines = [font.render(line, True, color) for line in lines]
        return rendered_lines

class Resource():
    def __init__(self, type, amount, x_pos):
            self.type = type
            self.amount = amount
            self.x_pos = x_pos
            self.current_amount = amount
    def update(self, current_amount):
            self.current_amount = min(self.amount, current_amount)
    def display(self, font):
            line = f"{self.type.capitalize()}: {self.current_amount}"
            line_surface = font.render(line, True, (255, 255, 255))
            line_rect = line_surface.get_rect(topleft = (self.x_pos+5, 5))
            return line_surface, line_rect

