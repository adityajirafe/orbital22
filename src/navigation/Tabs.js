import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import { MainScreen } from "../screens";

const Tab = createBottomTabNavigator();

const Tabs = () => {
    return (
        <Tab.Navigator>
            <Tab.Screen 
                name = 'Main'
                component={ MainScreen }
            />                     
        </Tab.Navigator>
    );
}

export default Tabs;

// work in progress