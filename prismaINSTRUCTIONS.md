In order to use prisma you need to run the following commands:

```
pip install prisma
prisma migrate deploy
prisma generate
```

If you change the schema.prisma, you need to create a new migration with:
```
prisma migrate dev
```