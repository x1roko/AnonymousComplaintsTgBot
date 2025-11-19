CREATE DATABASE IF NOT EXISTS `telegram_anon_db`
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE `telegram_anon_db`;


CREATE TABLE IF NOT EXISTS `anonymous_messages` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'Уникальный ID записи',
  
  -- Поле для хранения текста сообщения. TEXT подходит для сообщений любой длины.
  `message_text` TEXT NOT NULL COMMENT 'Сохраненный текст сообщения пользователя',
  
  -- Метка времени создания записи. Полезно для аудита, но не содержит личных данных.
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Дата и время сохранения сообщения',
  
  PRIMARY KEY (`id`)
)
ENGINE = InnoDB
COMMENT = 'Таблица для анонимного хранения текста сообщений от Telegram-пользователей';
