SELECT count(i1.Item_ID)
FROM Items AS i1
WHERE 4 IN (
	SELECT count(c1.Item_ID)
	FROM Categories AS c1
  WHERE i1.Item_ID = c1.Item_ID);