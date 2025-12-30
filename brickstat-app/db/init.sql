CREATE TABLE IF NOT EXISTS reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    set_num VARCHAR(20) NOT NULL,
    build_time_minutes INT NOT NULL,
    distraction_level INT NOT NULL,
    organization_level INT NOT NULL,
    build_speed INT NOT NULL,
    review_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sets(
    id INT AUTO_INCREMENT PRIMARY KEY,
    set_num VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    release_year INT,
    piece_count INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX (set_num)
);