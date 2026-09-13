-- =============================================================
-- MoMo SMS Analytics — MySQL Database Setup
-- Team: Brain Boosters
-- =============================================================

CREATE DATABASE IF NOT EXISTS momo_sms;
USE momo_sms;

-- -------------------------------------------------------------
-- 1. transaction_categories
--    Lookup table for the 7 known MoMo SMS categories.
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS transaction_categories (
    id          INT           UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT 'Surrogate PK',
    name        VARCHAR(50)   NOT NULL UNIQUE              COMMENT 'Category slug, e.g. incoming_money',
    description VARCHAR(255)  NOT NULL DEFAULT ''          COMMENT 'Human-readable explanation',
    created_at  DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_cat_name CHECK (name IN (
        'incoming_money','payment','transfer',
        'withdrawal','airtime','third_party_initiated','other'
    ))
) COMMENT='Lookup table for MoMo transaction categories';

CREATE INDEX idx_cat_name ON transaction_categories (name);


-- -------------------------------------------------------------
-- 2. users
--    Represents any phone number that appears as a party in
--    a transaction (sender, receiver, or account owner).
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    id           INT          UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT 'Surrogate PK',
    phone        VARCHAR(20)  NOT NULL UNIQUE COMMENT 'E.164 phone number, e.g. +250780000001',
    display_name VARCHAR(100) NOT NULL DEFAULT '' COMMENT 'Name extracted from SMS body when available',
    created_at   DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_phone_format CHECK (phone REGEXP '^\\+[0-9]{7,15}$')
) COMMENT='Phone-number-based user/party registry';

CREATE INDEX idx_user_phone ON users (phone);


-- -------------------------------------------------------------
-- 3. transactions
--    Core fact table — one row per unique SMS message.
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS transactions (
    id          INT           UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT 'Surrogate PK',
    user_id     INT           UNSIGNED NOT NULL               COMMENT 'FK → users.id (account owner)',
    category_id INT           UNSIGNED NOT NULL               COMMENT 'FK → transaction_categories.id',
    address     VARCHAR(20)   NOT NULL                        COMMENT 'Raw sender address from XML',
    date        DATETIME      NOT NULL                        COMMENT 'Transaction timestamp (UTC)',
    body        TEXT          NOT NULL                        COMMENT 'Original SMS text',
    amount      DECIMAL(15,2) NULL                            COMMENT 'Extracted RWF amount; NULL when not applicable',
    body_hash   CHAR(64)      NOT NULL UNIQUE                 COMMENT 'SHA-256 of body for deduplication',
    created_at  DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_tx_user     FOREIGN KEY (user_id)     REFERENCES users(id)                   ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_tx_category FOREIGN KEY (category_id) REFERENCES transaction_categories(id)  ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT chk_amount_pos CHECK (amount IS NULL OR amount >= 0)
) COMMENT='One row per unique MoMo SMS transaction';

CREATE INDEX idx_tx_user     ON transactions (user_id);
CREATE INDEX idx_tx_category ON transactions (category_id);
CREATE INDEX idx_tx_date     ON transactions (date);
CREATE INDEX idx_tx_amount   ON transactions (amount);


-- -------------------------------------------------------------
-- 4. transaction_parties  (junction — resolves M:N)
--    A single transaction can involve multiple parties
--    (e.g. sender AND receiver), and a user can appear in
--    many transactions.
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS transaction_parties (
    transaction_id INT          UNSIGNED NOT NULL COMMENT 'FK → transactions.id',
    user_id        INT          UNSIGNED NOT NULL COMMENT 'FK → users.id',
    role           VARCHAR(20)  NOT NULL          COMMENT 'Role: sender | receiver | agent | merchant',
    PRIMARY KEY (transaction_id, user_id, role),

    CONSTRAINT fk_tp_transaction FOREIGN KEY (transaction_id) REFERENCES transactions(id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_tp_user        FOREIGN KEY (user_id)        REFERENCES users(id)        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT chk_party_role    CHECK (role IN ('sender','receiver','agent','merchant'))
) COMMENT='Junction table resolving M:N between transactions and users';

CREATE INDEX idx_tp_user ON transaction_parties (user_id);


-- -------------------------------------------------------------
-- 5. system_logs
--    Tracks every ETL pipeline run and any per-record errors.
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS system_logs (
    id             INT          UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT 'Surrogate PK',
    transaction_id INT          UNSIGNED NULL                       COMMENT 'FK → transactions.id; NULL for pipeline-level events',
    level          VARCHAR(10)  NOT NULL DEFAULT 'INFO'             COMMENT 'INFO | WARNING | ERROR',
    event          VARCHAR(100) NOT NULL                            COMMENT 'Short event code, e.g. PARSE_FAILED',
    message        TEXT         NOT NULL DEFAULT ''                 COMMENT 'Detailed log message',
    created_at     DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_log_transaction FOREIGN KEY (transaction_id) REFERENCES transactions(id) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT chk_log_level      CHECK (level IN ('INFO','WARNING','ERROR'))
) COMMENT='ETL pipeline audit and error log';

CREATE INDEX idx_log_level      ON system_logs (level);
CREATE INDEX idx_log_created_at ON system_logs (created_at);


-- =============================================================
-- SAMPLE DATA  (5+ rows per main table)
-- =============================================================

-- transaction_categories
INSERT INTO transaction_categories (name, description) VALUES
    ('incoming_money',        'Money received from another MoMo user'),
    ('payment',               'Payment to a merchant or service provider'),
    ('transfer',              'Money sent to another MoMo user'),
    ('withdrawal',            'Cash withdrawn via an agent'),
    ('airtime',               'Airtime or data bundle purchase'),
    ('third_party_initiated', 'Transaction initiated by a third-party merchant'),
    ('other',                 'Uncategorised or informational SMS');

-- users
INSERT INTO users (phone, display_name) VALUES
    ('+250780000001', 'John Doe'),
    ('+250780000002', 'Kigali Supermarket'),
    ('+250780000003', 'Jane Smith'),
    ('+250780000004', 'Agent 00123'),
    ('+250780000005', 'PayGo Merchant'),
    ('+250780000099', 'Account Owner');

-- transactions  (body_hash uses SHA2 for demo; in production the ETL computes this)
INSERT INTO transactions (user_id, category_id, address, date, body, amount, body_hash) VALUES
    (6, 1, '250780000001', '2023-11-14 22:13:20',
     'You have received 5,000 RWF from John Doe. Your new balance is 15,000 RWF.',
     5000.00, SHA2('You have received 5,000 RWF from John Doe. Your new balance is 15,000 RWF.', 256)),

    (6, 2, '250780000002', '2023-11-14 23:13:20',
     'Payment of 2,500 RWF to Kigali Supermarket has been completed. Your new balance is 12,500 RWF.',
     2500.00, SHA2('Payment of 2,500 RWF to Kigali Supermarket has been completed. Your new balance is 12,500 RWF.', 256)),

    (6, 3, '250780000003', '2023-11-15 00:13:20',
     'You have transferred to 0780000099 3,000 RWF. Your new balance is 9,500 RWF.',
     3000.00, SHA2('You have transferred to 0780000099 3,000 RWF. Your new balance is 9,500 RWF.', 256)),

    (6, 4, '250780000004', '2023-11-15 01:13:20',
     'You have withdrawn 4,000 RWF from agent 00123. Your new balance is 5,500 RWF.',
     4000.00, SHA2('You have withdrawn 4,000 RWF from agent 00123. Your new balance is 5,500 RWF.', 256)),

    (6, 5, '250780000005', '2023-11-15 02:13:20',
     'You have purchased airtime worth 500 RWF. Your new balance is 5,000 RWF.',
     500.00,  SHA2('You have purchased airtime worth 500 RWF. Your new balance is 5,000 RWF.', 256)),

    (6, 6, '250780000005', '2023-11-15 03:13:20',
     'A transaction of 1,000 RWF was initiated by merchant PayGo on your account.',
     1000.00, SHA2('A transaction of 1,000 RWF was initiated by merchant PayGo on your account.', 256)),

    (6, 7, '250780000010', '2023-11-15 07:13:20',
     'Your OTP is 482910. Do not share this code with anyone.',
     NULL,    SHA2('Your OTP is 482910. Do not share this code with anyone.', 256));

-- transaction_parties  (who was involved in each transaction)
INSERT INTO transaction_parties (transaction_id, user_id, role) VALUES
    (1, 1, 'sender'),    -- John Doe sent money → tx 1
    (1, 6, 'receiver'),  -- Account Owner received → tx 1
    (2, 6, 'sender'),    -- Account Owner paid → tx 2
    (2, 2, 'merchant'),  -- Kigali Supermarket received → tx 2
    (3, 6, 'sender'),    -- Account Owner transferred → tx 3
    (3, 3, 'receiver'),  -- Jane Smith received → tx 3
    (4, 6, 'sender'),    -- Account Owner withdrew → tx 4
    (4, 4, 'agent'),     -- Agent 00123 facilitated → tx 4
    (5, 6, 'sender'),    -- Account Owner bought airtime → tx 5
    (6, 5, 'merchant');  -- PayGo initiated → tx 6

-- system_logs
INSERT INTO system_logs (transaction_id, level, event, message) VALUES
    (NULL, 'INFO',    'ETL_START',    'ETL pipeline started; source: data/raw/momo.xml'),
    (NULL, 'INFO',    'PARSE_OK',     'Parsed 10 SMS records from XML'),
    (7,    'WARNING', 'AMOUNT_NULL',  'No RWF amount found in body; amount set to NULL'),
    (NULL, 'INFO',    'LOAD_OK',      'Inserted 7 records into transactions table'),
    (NULL, 'ERROR',   'DUPLICATE_SK', 'Skipped 3 duplicate body values during upsert');


-- =============================================================
-- SAMPLE CRUD QUERIES
-- =============================================================

-- READ: all transactions with category name and owner phone
SELECT t.id, u.phone AS owner, tc.name AS category, t.amount, t.date
FROM   transactions t
JOIN   users u                   ON t.user_id     = u.id
JOIN   transaction_categories tc ON t.category_id = tc.id
ORDER  BY t.date;

-- READ: total amount and count per category
SELECT tc.name AS category, COUNT(*) AS tx_count, SUM(t.amount) AS total_rwf
FROM   transactions t
JOIN   transaction_categories tc ON t.category_id = tc.id
GROUP  BY tc.name
ORDER  BY total_rwf DESC;

-- READ: all parties involved in transaction #1
SELECT u.phone, u.display_name, tp.role
FROM   transaction_parties tp
JOIN   users u ON tp.user_id = u.id
WHERE  tp.transaction_id = 1;

-- UPDATE: correct a display name
UPDATE users SET display_name = 'John Doe (Updated)' WHERE phone = '+250780000001';

-- DELETE: remove a log entry (soft-delete pattern not needed for logs)
DELETE FROM system_logs WHERE event = 'DUPLICATE_SK' AND level = 'ERROR';
