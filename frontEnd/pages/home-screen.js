import { StatusBar } from 'expo-status-bar';
import React from 'react';
import { useState, useEffect} from 'react'
import { StyleSheet, Text, View, SafeAreaView, FlatList, Image, ScrollView, TouchableOpacity} from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { LinearGradient } from 'expo-linear-gradient';

function HomeScreen({ navigation }) {
  const Item = ({ name, interest, imgurl}) => (
    <TouchableOpacity
      onPress={() => navigation.navigate('Profile')}
      style={styles.container, styles.card}>
      <Text style={styles.titletext}>{name}</Text>
        <View style={styles.flexrow}>
          <Image style={styles.image} source={require('../assets/default_avatar.png')}/>
          <Text style={styles.title}>{interest}</Text>
        </View>
    </TouchableOpacity>
  );

  const [matchData, setMatchdata] =  useState({ data: {} });
  const [matchList, setMatchlist] =  useState({ data: {} });

  const token = window.localStorage.getItem('token');

  useEffect(() => {
    fetch(`http://137.184.103.104:8000/statboard?token_user=${token}`
    )
    .then(response => response.json())
    .then(data => {
      console.log('Success:', data);
      setMatchdata(data)
    })
    .catch((error) => {
      console.error('Error:', error);
    });
  }, [token]);

  useEffect(() => {
      fetch(`http://137.184.103.104:8000/matches/recommendations/cards?token_user=${token}`
      )
      .then(response => response.json())
      .then(data => {
          console.log('Success:', data);
          setMatchlist(data);
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  }, [token]);

const renderItem = ({ item }) => (
  <Item name={item.full_name} interest={item.major_match_interest} />
);

  return (
    <View style={{ flex: 1 }}>
      <LinearGradient colors={['#FFAFBD', '#ffc3a0']} style={styles.gradient}>

    <View style={styles.section}>
      <View style={styles.container}>
        <Text style={styles.titletext}>
          Activity
        </Text>
        <View>
          <Text style={styles.stat}>
            Active Matches {matchData.number_active_matches}
          </Text>
        </View>
        <View>
          <Text style={styles.stat}>
            Outgoing Matches {matchData.number_outgoing_matches}
          </Text>
        </View>
        <View>
          <Text style={styles.stat}>
            Incoming Matches {matchData.number_incoming_matches}
          </Text>
        </View>
      </View>
    </View>

      <View style={styles.section}>
        <View style={styles.container}>
          <Text style={styles.titletext}>
            Matches
          </Text>
        </View>

        <SafeAreaView style={styles.viewStyle}>
            
             <FlatList
               style={styles.flexrow}
               data={matchList}
               renderItem={renderItem}
               keyExtractor={item => item.uid}
               numColumns={4}
               showsHorizontalScrollIndicator={false}
             />
        </SafeAreaView>
      </View>
      </LinearGradient>
    </View>
  );
}

const styles = StyleSheet.create({
  viewStyle: {
    padding: 10,
    margin: "auto",
    borderRadius: 7,
    width: '80%',
  },
  container: {
    backgroundColor: '#fff',
    padding: 10,
    margin: "auto",
    borderRadius: 7,
    width: '80%',
  },
  titletext: {
    color: '#EC6F66',
    fontSize: 20,
    borderBottomWidth: 2,
    borderBottomColor: "#DDD",
    padding: 5,
    marginBottom: 10,
  },
  stat: {
    color: 'white',
    backgroundColor: '#EC6F66',
    padding: 5,
    marginTop: 20,
    fontSize: 20,
    borderRadius: 5,

  },
  image: {
    height: 110,
    width: 110,
    backgroundColor: 'aliceblue',
    marginRight: 10,
  },
  flexrow: {
    overflowX: 'scroll',
    flexDirection: 'row',
  },
  card: {
    padding: 10,
    backgroundColor: 'white',
    width: '30%',
    borderRadius: 10,
    marginRight: 20,
    borderColor: '#EC6F66',
    borderWidth: 2,
  },
  section: {
    flex: 1,
  },
  gradient: {
    flex: 1,
  }
});

export default HomeScreen
