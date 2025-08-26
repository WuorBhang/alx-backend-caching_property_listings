# ALX Backend Caching Property Listings

A Django-based property listing application with Redis caching at multiple levels. This project demonstrates various caching strategies including view-level caching, low-level queryset caching, and proper cache invalidation techniques.

## Features

- **Multi-level Caching**: View-level caching (15 minutes) and low-level queryset caching (1 hour)
- **Redis Integration**: Uses Redis as the cache backend for high performance
- **Cache Invalidation**: Automatic cache invalidation using Django signals
- **Cache Metrics**: Real-time Redis cache performance monitoring
- **Docker Support**: Containerized PostgreSQL and Redis services
- **Property Management**: Full CRUD operations for property listings

## Architecture

- **Django 4.2.7**: Web framework
- **PostgreSQL**: Primary database
- **Redis**: Cache backend and session storage
- **Docker**: Service containerization

## Setup Instructions

### Prerequisites

- Python 3.8+
- Docker and Docker Compose
- pip (Python package manager)

### 1. Clone the Repository

```bash
git clone https://github.com/WuorBhang/alx-backend-caching_property_listings.git
cd alx-backend-caching_property_listings
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Start Docker Services

```bash
docker-compose up -d
```

This will start:
- PostgreSQL on port 5432
- Redis on port 6379

### 5. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 7. Run the Development Server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## API Endpoints

### Properties

- **GET** `/properties/` - List all properties (cached for 15 minutes)
- **GET** `/properties/metrics/` - View Redis cache performance metrics

### Admin

- **GET** `/admin/` - Django admin interface for property management

## Caching Strategy

### View-Level Caching
- **Duration**: 15 minutes
- **Scope**: Entire view response
- **Implementation**: `@cache_page(60 * 15)` decorator

### Low-Level Caching
- **Duration**: 1 hour
- **Scope**: Property queryset
- **Implementation**: `cache.set('all_properties', queryset, 3600)`

### Cache Invalidation
- **Triggers**: Property create, update, delete
- **Method**: Django signals (`post_save`, `post_delete`)
- **Action**: Automatic deletion of `all_properties` cache key

## Cache Metrics

The application provides real-time Redis cache performance metrics including:

- Cache hit/miss ratios
- Total request counts
- Cache size and memory usage
- Performance logging

## Docker Services

### PostgreSQL
- **Image**: `postgres:latest`
- **Port**: 5432
- **Database**: `property_db`
- **User**: `property_user`
- **Password**: `property_password`

### Redis
- **Image**: `redis:latest`
- **Port**: 6379
- **Purpose**: Caching and session storage

## Development

### Adding New Properties

1. Access Django admin at `/admin/`
2. Navigate to Properties section
3. Add new property with title, description, price, and location
4. Cache will automatically invalidate

### Monitoring Cache Performance

1. Visit `/properties/metrics/` to view real-time metrics
2. Check Django logs for cache hit/miss information
3. Monitor Redis memory usage and key counts

## Testing

### Manual Testing

1. Visit `/properties/` multiple times to test view caching
2. Add/modify properties to test cache invalidation
3. Check `/properties/metrics/` for performance data

### Cache Testing

1. First request: Should show "Cache MISS" in logs
2. Subsequent requests: Should show "Cache HIT" in logs
3. After property changes: Cache should invalidate automatically

## Troubleshooting

### Common Issues

1. **Database Connection Error**: Ensure Docker services are running
2. **Redis Connection Error**: Check Redis service status
3. **Migration Errors**: Delete database volume and recreate

### Reset Services

```bash
docker-compose down -v
docker-compose up -d
```

## Performance Benefits

- **Reduced Database Load**: Cached responses eliminate repeated queries
- **Faster Response Times**: Redis provides sub-millisecond access
- **Scalability**: Cache layer handles increased traffic efficiently
- **Cost Optimization**: Reduced database infrastructure requirements

## Production Considerations

- Use Redis persistence for data durability
- Implement cache warming strategies
- Monitor cache hit ratios for optimization
- Consider Redis clustering for high availability
- Use environment variables for sensitive configuration

## License

This project is part of the ALX Backend Development curriculum.
