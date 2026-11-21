import {Bar,BarChart,CartesianGrid,ResponsiveContainer,Tooltip,XAxis,YAxis} from 'recharts';
import type {Analytics} from './api';

/** Loaded only when Teacher Insights is visited to keep student routes light. */
export default function TeacherChart({analytics}:{analytics:Analytics|null}){
  return <div className="chart-box"><ResponsiveContainer width="100%" height="100%"><BarChart data={analytics?.concepts.filter(c=>c.avg_mastery!==null)||[]} layout="vertical" margin={{left:6,right:24}}><CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#ECE8E0"/><XAxis type="number" domain={[0,100]}/><YAxis type="category" dataKey="title" width={105} tick={{fontSize:11}}/><Tooltip/><Bar dataKey="avg_mastery" name="Avg mastery (%)" fill="#BD47F2" radius={[0,8,8,0]} barSize={21}/></BarChart></ResponsiveContainer></div>
}
