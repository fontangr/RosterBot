-- name: set_vaga(vaga,discord_user,discord_user_id,discord_guild_id, universo)!
-- Insere uma nova vaga pra um usuário. Lança IntegrityError se já existir (guild_id + vaga duplicados).
INSERT INTO rpg_local_register(vaga,discord_user,discord_user_id,discord_guild_id,universo)
VALUES (:vaga, :discord_user, :discord_user_id, :discord_guild_id,:universo);

-- name: get_vaga(discord_guild_id,vaga)^
-- Busca uma vaga específica dentro de uma guild. Retorna uma linha ou None.
SELECT vaga, discord_user, discord_user_id, discord_guild_id
FROM rpg_local_register
WHERE discord_guild_id = :discord_guild_id AND vaga = :vaga;

-- name: drop_vaga(discord_guild_id,vaga)!
-- Apaga uma vaga específica de uma guild.
DELETE FROM rpg_local_register
WHERE discord_guild_id = :discord_guild_id AND vaga = :vaga;

-- name: replace_vaga(discord_user_id,discord_guild_id,vaga_substituicao,universo)!
-- Troca a vaga de um usuário (localizado por guild_id + user_id) pra outra vaga.
UPDATE rpg_local_register
SET vaga = :vaga_substituicao,universo = :universo
WHERE discord_guild_id = :discord_guild_id AND discord_user_id = :discord_user_id;

-- name: listar_vagas(discord_guild_id)
-- Lista todas as vagas ocupadas de uma guild.
SELECT discord_user, vaga
FROM rpg_local_register
WHERE discord_guild_id = :discord_guild_id;


-- name: verificar_pessoa(discord_user_id,discord_guild_id)
-- Busca por uma vaga que esteja registrada com o discord_user_id e no mesmo servidor.
SELECT vaga
FROM rpg_local_register
WHERE discord_user_id = :discord_user_id AND discord_guild_id = :discord_guild_id