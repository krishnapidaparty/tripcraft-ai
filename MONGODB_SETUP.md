# MongoDB Setup Guide for TripCraft AI

## 🗄️ MongoDB Integration Overview

TripCraft AI now uses MongoDB to store:
- User sessions and preferences
- Generated travel plans
- Chat history
- Destination data

## 🚀 Quick Setup Options

### Option 1: MongoDB Atlas (Recommended - Cloud)
**Best for:** Production, sharing, no local setup required

1. **Create MongoDB Atlas Account**
   - Go to [MongoDB Atlas](https://www.mongodb.com/atlas)
   - Sign up for free account

2. **Create Free Cluster**
   - Click "Build a Database"
   - Choose "FREE" tier (M0)
   - Select cloud provider (AWS/Google Cloud/Azure)
   - Choose region closest to you
   - Click "Create"

3. **Set Up Database Access**
   - Go to "Database Access" in left sidebar
   - Click "Add New Database User"
   - Username: `tripcraft_user`
   - Password: Generate strong password
   - **Save the password!**

4. **Set Up Network Access**
   - Go to "Network Access" in left sidebar
   - Click "Add IP Address"
   - Click "Allow Access from Anywhere" (for development)
   - Click "Confirm"

5. **Get Connection String**
   - Click "Connect" on your cluster
   - Choose "Connect your application"
   - Copy the connection string
   - Replace `<password>` with your actual password

6. **Update Environment Variables**
   ```bash
   # Edit your .env file
   MONGODB_URL=mongodb+srv://tripcraft_user:your_password@cluster0.xxxxx.mongodb.net/tripcraft_ai?retryWrites=true&w=majority
   ```

### Option 2: Local MongoDB
**Best for:** Development, offline work

1. **Install MongoDB**
   ```bash
   # macOS
   brew install mongodb-community
   
   # Ubuntu/Debian
   sudo apt-get install mongodb
   
   # Windows
   # Download from mongodb.com
   ```

2. **Start MongoDB**
   ```bash
   # macOS
   brew services start mongodb-community
   
   # Ubuntu/Debian
   sudo systemctl start mongodb
   
   # Windows
   # Start MongoDB service
   ```

3. **Verify Installation**
   ```bash
   mongosh
   # Should connect to MongoDB shell
   ```

## 🧪 Testing Your Setup

Run the MongoDB test script:

```bash
python test_mongodb.py
```

Expected output:
```
🔍 Testing MongoDB Connection...
✅ Connected to MongoDB successfully!
✅ Created user session: test_session_123
✅ Retrieved session: test_session_123
✅ Updated session successfully
✅ Database collections: ['sessions', 'travel_plans', 'chat_messages', 'destinations']
🎉 All MongoDB tests passed!
🔌 MongoDB connection closed
```

## 🔧 Environment Variables

### Required Variables
```env
MONGODB_URL=mongodb://localhost:27017  # Local MongoDB
# or
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/tripcraft_ai  # Atlas
```

### Optional Variables
```env
MONGODB_DATABASE_NAME=tripcraft_ai  # Default database name
```

## 🌐 Deployment Configuration

### Replit
The `.replit` file already includes MongoDB environment variables.

### Heroku
```bash
heroku config:set MONGODB_URL="your_mongodb_atlas_connection_string"
```

### Railway
Add `MONGODB_URL` to your environment variables in Railway dashboard.

### Vercel
Add `MONGODB_URL` to your environment variables in Vercel dashboard.

## 📊 Database Collections

Your MongoDB database will automatically create these collections:

- **sessions** - User session data
- **travel_plans** - Generated itineraries
- **chat_messages** - Chat history
- **destinations** - Destination information

## 🔍 Troubleshooting

### Connection Issues
1. **Check MONGODB_URL** - Verify connection string is correct
2. **Network Access** - Ensure IP is whitelisted in Atlas
3. **Credentials** - Verify username/password
4. **Database Name** - Check if database name is included in URL

### Common Errors
- `ServerSelectionTimeoutError` - Network connectivity issue
- `AuthenticationFailed` - Wrong username/password
- `OperationFailure` - Insufficient permissions

### Performance Tips
- Use MongoDB Atlas for production
- Enable connection pooling
- Index frequently queried fields
- Monitor database usage

## 📈 Monitoring

### MongoDB Atlas Dashboard
- Monitor cluster performance
- View connection metrics
- Check storage usage
- Set up alerts

### Application Logs
Check your application logs for MongoDB-related errors:
```bash
tail -f logs/app.log | grep -i mongo
```

## 🔐 Security Best Practices

1. **Use Strong Passwords** - Generate complex passwords for database users
2. **Network Security** - Restrict IP access in production
3. **Encryption** - Use TLS/SSL connections
4. **Regular Backups** - Enable automated backups in Atlas
5. **Access Control** - Use least privilege principle

## 📚 Additional Resources

- [MongoDB Documentation](https://docs.mongodb.com/)
- [MongoDB Atlas Guide](https://docs.atlas.mongodb.com/)
- [Motor (Async MongoDB Driver)](https://motor.readthedocs.io/)
- [PyMongo Documentation](https://pymongo.readthedocs.io/)

---

**Need help?** Check the troubleshooting section or create an issue in the repository.
