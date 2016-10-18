SELECT e.base_name, e.date, s.name, g.name, a.name, p.skeletons_file, p.features_file, p.n_timestamps
FROM experiments e 
JOIN strains s ON e.strain_id = s.id 
JOIN genes g ON g.id = s.gene_id 
JOIN alleles a ON a.id = s.allele_id 
JOIN progress_tracks p ON e.id = p.experiment_id
WHERE e.sex_id = (SELECT id FROM sexes WHERE name = 'hermaphrodite') 
AND e.developmental_stage_id = (SELECT id FROM developmental_stages WHERE name = 'young adult') 
AND e.food_id = (SELECT id FROM foods WHERE name = 'OP50') 
AND e.arena_id = (SELECT id FROM arenas WHERE name NOT LIKE '%liquid%')
AND e.habituation_id = (SELECT id FROM habituations WHERE name = '30 minutes')
AND (g.id IN (SELECT id FROM genes WHERE name IN ('trp-4', 'unc-9')) 
OR s.id = (SELECT id FROM strains WHERE name = 'N2'))
AND (base_name LIKE 'N2%' OR base_name LIKE 'trp-4%' OR base_name LIKE 'unc-9%')
AND p.exit_flag_id = (SELECT id FROM exit_flags WHERE name = 'Finished')
AND p.n_timestamps BETWEEN 20000 AND 30000;


