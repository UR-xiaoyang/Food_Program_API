CREATE TABLE log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    operation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    operation VARCHAR(255) NOT NULL,
    ip_address VARCHAR(45) NOT NULL,
    user VARCHAR(255) NOT NULL
);

CREATE TABLE user (
    ID INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL,
    2fa_key VARCHAR(255),
    PRIMARY KEY (ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS verification_code (
    id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL,
    code VARCHAR(255) NOT NULL,
    ip_address VARCHAR(255),
    used VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE users_data (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '用户ID，自增主键',           -- 用户ID
    user_id VARCHAR(36) COMMENT '用户唯一标识（UUID或其他唯一值）', -- 用户唯一标识
    age INT COMMENT '用户年龄，必填字段',                          -- 年龄
    gender VARCHAR(10) COMMENT '用户性别，例如：男、女',            -- 性别
    weight DECIMAL(5,2) COMMENT '用户体重（单位kg），保留两位小数',   -- 体重
    height DECIMAL(5,2) COMMENT '用户身高（单位cm），保留两位小数',   -- 身高
    health_status VARCHAR(50) COMMENT '用户的健康状况描述，例如：良好、一般',  -- 健康状况
    diet_preference VARCHAR(50) COMMENT '用户的饮食偏好，例如：低碳水化合物' -- 饮食偏好
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='存储用户基本信息的表';

CREATE TABLE plans (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    time DATE NOT NULL,
    data JSON,  -- 存储计划内容表的ID列表
    user_id VARCHAR(255) NOT NULL
);

CREATE TABLE plan_contents (
    ID CHAR(36) PRIMARY KEY,
    content TEXT NOT NULL,
    is_completed BOOLEAN DEFAULT FALSE
);

CREATE TABLE nutrition_data (
    data_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    protein FLOAT NOT NULL,
    carbohydrates FLOAT NOT NULL,
    fat FLOAT NOT NULL,
    fiber FLOAT NOT NULL,
    vitamin_c FLOAT NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE plan_nutrition (
    data_id INT PRIMARY KEY AUTO_INCREMENT,
    plan_contents_uuid char(36) NOT NULL,
    protein FLOAT NOT NULL,
    carbohydrates FLOAT NOT NULL,
    fat FLOAT NOT NULL,
    fiber FLOAT NOT NULL,
    vitamin_c FLOAT NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
