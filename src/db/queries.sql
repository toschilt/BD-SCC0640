-- QUERY 2
-- Obter todos os alunos e, caso eles sejam orientados por algum professor, também mostrar os dados do professor.

SELECT a.cpf, a.procurando_moradia, o.professor
FROM aluno a LEFT JOIN orienta o
ON a.cpf = o.aluno;

-- QUERY 3
-- Dada uma festa, verificar quantos moradores existem em uma moradia na data da festa.

-- Pegar a moradia em que ocorre uma festa
SELECT f.moradia FROM festa f
WHERE f.nome = 'Indy Festa';

-- Pegar todas as pessoas que moraram na moradia
SELECT c.locatario FROM festa f JOIN contrato_aluguel c
ON c.residencia = f.moradia 
WHERE f.nome = 'Indy Festa';

-- Pegar todos os moradores que moravam la durante a festa
SELECT COUNT(c.locatario) as qte_moradores FROM festa f JOIN contrato_aluguel c
ON c.residencia = f.moradia 
WHERE c.inicio < DATE(f.data_horario) AND c.fim > DATE(f.data_horario)
AND f.nome = 'Indy Festa';

-- TODO Adicionar mais dados para essa moradia


-- QUERY 4



-- QUERY 7
-- Quais são os alunos que foram em todas as palestras de um determinado professor e não são orientados por nenhum ainda?

-- Para pegar o CPF de todos os alunos que não são orientados
SELECT a.CPF FROM aluno a LEFT JOIN orienta o 
ON a.cpf = o.aluno WHERE o.aluno IS NULL;

-- Para pegar todas as palestras dadas por um professor
SELECT id FROM palestra WHERE ministrante = '74214010591'

-- Para pegar todos os alunos que participaram de todas as palestras de um professor
SELECT CPF FROM aluno a WHERE 
NOT EXISTS (
    (SELECT id FROM palestra WHERE ministrante = '74214010591')
    EXCEPT 
    (SELECT palestra FROM presenca_marcada WHERE aluno = a.CPF)
);

-- Pegar todos os alunos não orientados que participam da palestra
SELECT a.CPF FROM aluno a LEFT JOIN orienta o 
ON a.cpf = o.aluno WHERE o.aluno IS NULL AND
NOT EXISTS (
    (SELECT id FROM palestra WHERE ministrante = '74214010591')
    EXCEPT 
    (SELECT palestra FROM presenca_marcada WHERE aluno = a.CPF)
);
